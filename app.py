import streamlit as st
import folium
import ee
from utils import initialize_gee
import streamlit.components.v1 as components
import json

# Page Config
st.set_page_config(layout="wide", page_title="Mataram SSTB - Smart Tax Inspector")

st.markdown("""
<style>
    .reportview-container { margin-top: -2em; }
    #map_div { width: 100%; height: 750px; }
    .demo-badge {
        position: fixed;
        top: 60px;
        right: 20px;
        background: #ff6b6b;
        color: white;
        padding: 10px 20px;
        border-radius: 20px;
        font-weight: bold;
        z-index: 9999;
    }
    .height-legend {
        padding: 15px;
        background: white;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.15);
        margin: 10px 0;
    }
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

st.title("🛰️ Mataram SSTB: Precision Tax Inspector Pro")
st.markdown("**Core Engine**: Google Earth High-Res Satellite + Open Buildings V3 AI + **DSM Height Detection** 🏢")

# Check for demo mode
demo_mode = st.session_state.get('demo_mode', False)

# --- SIDEBAR ---
st.sidebar.header("🕹️ Tax Configuration")
tax_rate = st.sidebar.number_input("Tax Rate (Rp / m²)", value=5000, step=500)
inspector_radius = st.sidebar.slider("Inspector Radius (meters)", 100, 1000, 500)

st.sidebar.header("🏢 Height Detection")
show_height_colors = st.sidebar.checkbox("🎨 Aktifkan Indikasi Ketinggian", value=False,
                                         help="ON: Warna sesuai tinggi | OFF: Outline merah saja")
height_tax_multiplier = st.sidebar.slider("Height Tax Multiplier", 1.0, 3.0, 1.5, 0.1,
                                          help="Taller buildings get higher tax")

# NEW: DSM Method Selection
st.sidebar.header("📐 Metode Pengukuran Tinggi")
height_method = st.sidebar.radio(
    "Pilih Metode:",
    ["Estimasi dari Luas Area", "DSM (Digital Surface Model)", "Hybrid (Cepat + Akurat)"],
    index=2,  # Default to Hybrid
    help="Hybrid: DSM untuk bangunan besar, estimasi untuk kecil (RECOMMENDED)"
)

if height_method == "Hybrid (Cepat + Akurat)":
    st.sidebar.success("✅ Mode Hybrid: Cepat & Akurat!")
    dsm_threshold = st.sidebar.slider("DSM untuk bangunan > (m²)", 100, 500, 200,
                                      help="Bangunan lebih besar dari ini akan pakai DSM")
elif height_method == "DSM (Digital Surface Model)":
    st.sidebar.warning("⚠️ Mode DSM: Akurat tapi lambat")
    dsm_threshold = 0  # All buildings use DSM

st.sidebar.header("🗺️ Map Settings")
initial_zoom = st.sidebar.slider("Initial Zoom Level", 15, 21, 19, 
                                  help="Higher = more zoomed in (max 21 for building details)")

# Option to load all buildings
load_all = st.sidebar.checkbox("🚀 Muat SEMUA Bangunan", value=False,
                                help="WARNING: Bisa sangat lambat! Akan memuat semua bangunan tanpa limit")

if load_all:
    max_buildings = 5000  # Very high limit
    st.sidebar.warning("⚠️ Mode ALL: Memuat hingga 5000 bangunan (bisa lambat)")
else:
    max_buildings = st.sidebar.slider("Max Buildings to Load", 100, 2000, 1000,
                                       help="Lebih banyak = lebih lengkap tapi lebih lambat")

# ROI
MATARAM_COORDS = [-8.5831, 116.1165]

# --- MAIN UI TABS ---
tab_map, tab_stats = st.tabs(["🗺️ Map & Inspector", "📊 Data Analysis & Reports"])

# --- SIDEBAR FILTERS ---
st.sidebar.header("🔍 Advanced Filters")
filter_min_area = st.sidebar.number_input("Min Area (m²)", 0, 1000, 0)
filter_max_area = st.sidebar.number_input("Max Area (m²)", 0, 5000, 5000)
filter_category = st.sidebar.multiselect(
    "Filter Kategori Tinggi",
    ["Rendah", "Sedang", "Tinggi", "Gedung"],
    default=["Rendah", "Sedang", "Tinggi", "Gedung"]
)

# Height classification function
def classify_height(height_m):
    """Classify building by height and return color and info"""
    if height_m < 5:
        return {
            'color': '#22c55e',  # Green
            'fill_color': '#22c55e',
            'category': 'Rendah',
            'floors': '1-2',
            'multiplier': 1.0,
            'emoji': '🏠'
        }
    elif height_m < 10:
        return {
            'color': '#eab308',  # Yellow
            'fill_color': '#fef08a',
            'category': 'Sedang',
            'floors': '2-3',
            'multiplier': 1.3,
            'emoji': '🏘️'
        }
    elif height_m < 15:
        return {
            'color': '#f97316',  # Orange
            'fill_color': '#fed7aa',
            'category': 'Tinggi',
            'floors': '3-5',
            'multiplier': 1.6,
            'emoji': '🏢'
        }
    else:
        return {
            'color': '#ef4444',  # Red
            'fill_color': '#fecaca',
            'category': 'Gedung',
            'floors': '5+',
            'multiplier': 2.0,
            'emoji': '🏬'
        }

def estimate_height_from_area(area):
    """Estimate building height from area (fallback method)"""
    if area < 80:
        return 3.5  # Small buildings: likely 1 floor residential
    elif area < 150:
        return 4.5  # Medium residential: 1-2 floors
    elif area < 250:
        return 7.5  # Larger buildings: likely 2-3 floors
    elif area < 400:
        return 12.0  # Large buildings: likely commercial 3-4 floors
    else:
        return 18.0  # Very large: likely multi-story commercial/office

def get_building_height_from_dsm(geometry, dsm, dtm):
    """
    Extract building height from DSM
    DSM = Digital Surface Model (top of buildings)
    DTM = Digital Terrain Model (ground level)
    Height = DSM - DTM
    """
    try:
        # Sample DSM and DTM at building location
        dsm_value = dsm.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=geometry,
            scale=30,
            maxPixels=1e9
        ).get('elevation')
        
        dtm_value = dtm.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=geometry,
            scale=30,
            maxPixels=1e9
        ).get('elevation')
        
        # Calculate height
        if dsm_value and dtm_value:
            dsm_val = ee.Number(dsm_value).getInfo()
            dtm_val = ee.Number(dtm_value).getInfo()
            height = max(0, dsm_val - dtm_val)
            
            # Sanity check: building height should be reasonable
            if height > 0.5 and height < 200:  # Between 0.5m and 200m
                return height
        
        return None
    except:
        return None

def create_building_popup(building_data, tax_rate, height_tax_multiplier, method=""):
    """Create detailed popup HTML for building"""
    height_info = classify_height(building_data['height'])
    tax_mult = height_info['multiplier'] * height_tax_multiplier
    base_tax = building_data['area'] * tax_rate
    total_tax = base_tax * tax_mult
    
    method_badge = ""
    if method == "DSM":
        method_badge = "<span style='background: #3b82f6; color: white; padding: 2px 6px; border-radius: 3px; font-size: 10px;'>DSM</span>"
    elif method == "Estimasi":
        method_badge = "<span style='background: #9ca3af; color: white; padding: 2px 6px; border-radius: 3px; font-size: 10px;'>EST</span>"
    
    html = f"""
    <div style='width: 280px; font-family: Arial, sans-serif;'>
        <h3 style='margin: 0 0 10px 0; color: #1f2937; border-bottom: 2px solid {height_info['color']}; padding-bottom: 5px;'>
            {height_info['emoji']} Informasi Bangunan {method_badge}
        </h3>
        
        <table style='width: 100%; font-size: 13px;'>
            <tr style='background: #f3f4f6;'>
                <td style='padding: 8px; font-weight: bold;'>📏 Luas Area</td>
                <td style='padding: 8px;'>{building_data['area']:.1f} m²</td>
            </tr>
            <tr>
                <td style='padding: 8px; font-weight: bold;'>📐 Tinggi Bangunan</td>
                <td style='padding: 8px; color: {height_info['color']}; font-weight: bold;'>{building_data['height']:.1f} meter</td>
            </tr>
            <tr style='background: #f3f4f6;'>
                <td style='padding: 8px; font-weight: bold;'>🏗️ Perkiraan Lantai</td>
                <td style='padding: 8px;'>{height_info['floors']} lantai</td>
            </tr>
            <tr>
                <td style='padding: 8px; font-weight: bold;'>📊 Kategori</td>
                <td style='padding: 8px;'><span style='background: {height_info['fill_color']}; padding: 2px 8px; border-radius: 4px; color: #1f2937; font-weight: bold;'>{height_info['category']}</span></td>
            </tr>
            <tr style='background: #f3f4f6;'>
                <td style='padding: 8px; font-weight: bold;'>📍 Koordinat</td>
                <td style='padding: 8px; font-size: 11px;'>{building_data['lat']:.5f}, {building_data['lon']:.5f}</td>
            </tr>
        </table>
        
        <div style='margin-top: 15px; padding: 10px; background: #eff6ff; border-radius: 5px; border-left: 4px solid #3b82f6;'>
            <div style='font-weight: bold; color: #1e40af; margin-bottom: 5px;'>💰 Perhitungan Pajak:</div>
            <div style='font-size: 12px; color: #1f2937;'>
                Tarif Dasar: Rp {tax_rate:,}/m²<br>
                Pajak Dasar: Rp {int(base_tax):,}<br>
                Faktor Tinggi: {tax_mult:.2f}x<br>
                <div style='margin-top: 5px; padding-top: 5px; border-top: 1px solid #bfdbfe;'>
                    <b style='color: #1e40af; font-size: 14px;'>Total Pajak: Rp {int(total_tax):,}</b>
                </div>
            </div>
        </div>
    </div>
    """
    return html

# --- DEMO MODE ---
if demo_mode:
    st.markdown('<div class="demo-badge">🎮 DEMO MODE</div>', unsafe_allow_html=True)
    st.info("📍 Mode simulasi dengan data sampel untuk demonstrasi fitur lengkap")
    
    # Create demo map with maximum zoom
    m = folium.Map(
        location=MATARAM_COORDS, 
        zoom_start=initial_zoom,
        max_zoom=21,
        tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr='Google Satellite'
    )
    
    # Sample Buildings with realistic data
    import random
    random.seed(42)
    
    sample_buildings = []
    base_lat, base_lon = MATARAM_COORDS
    
    # Generate 30 sample buildings around the area
    for i in range(30):
        offset_lat = random.uniform(-0.002, 0.002)
        offset_lon = random.uniform(-0.002, 0.002)
        
        building = {
            'lat': base_lat + offset_lat,
            'lon': base_lon + offset_lon,
            'area': random.uniform(50, 300),
            'height': random.choice([3.5, 4.0, 4.5, 6.0, 7.5, 9.0, 12.0, 15.0, 18.0, 21.0]),
            'id': f'BLD-{i+1:03d}'
        }
        sample_buildings.append(building)
    
    total_area = 0
    total_tax = 0
    height_distribution = {'Rendah': 0, 'Sedang': 0, 'Tinggi': 0, 'Gedung': 0}
    
    for building in sample_buildings:
        height_info = classify_height(building['height'])
        height_distribution[height_info['category']] += 1
        
        tax_mult = height_info['multiplier'] * height_tax_multiplier
        tax = building['area'] * tax_rate * tax_mult
        total_area += building['area']
        total_tax += tax
        
        # Create building footprint polygon (rectangular)
        size = (building['area'] ** 0.5) / 111000  # Approximate size in degrees
        coords = [
            [building['lat'] - size/2, building['lon'] - size/2],
            [building['lat'] - size/2, building['lon'] + size/2],
            [building['lat'] + size/2, building['lon'] + size/2],
            [building['lat'] + size/2, building['lon'] - size/2],
        ]
        
        # Add polygon with color based on toggle
        if show_height_colors:
            # Mode: Warna klasifikasi tinggi
            polygon_color = height_info['color']
            polygon_fill = True
            polygon_fill_color = height_info['fill_color']
            polygon_fill_opacity = 0.7
        else:
            # Mode: Outline merah saja
            polygon_color = '#ff0000'
            polygon_fill = False
            polygon_fill_color = '#ff0000'
            polygon_fill_opacity = 0
        
        folium.Polygon(
            locations=coords,
            popup=folium.Popup(
                create_building_popup(building, tax_rate, height_tax_multiplier, "Demo"),
                max_width=300
            ),
            tooltip=f"{height_info['emoji']} {height_info['category']} - {building['height']:.1f}m - Klik untuk detail",
            color=polygon_color,
            fill=polygon_fill,
            fillColor=polygon_fill_color,
            fillOpacity=polygon_fill_opacity,
            weight=2,
            opacity=1
        ).add_to(m)
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🏢 Total Bangunan", len(sample_buildings))
    col2.metric("📏 Total Area", f"{int(total_area):,} m²")
    col3.metric("📐 Rata-rata Tinggi", f"{sum(b['height'] for b in sample_buildings) / len(sample_buildings):.1f} m")
    col4.metric("💰 Potensi Pajak", f"Rp {int(total_tax):,}")
    
    # Distribution chart
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Height legend
        st.markdown(f"""
        <div class="height-legend">
            <b style='font-size: 16px;'>🏢 Klasifikasi Tinggi Bangunan:</b><br><br>
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 10px;'>
                <div style='padding: 10px; background: #dcfce7; border-left: 4px solid #22c55e; border-radius: 5px;'>
                    <b>🏠 Rendah</b><br>
                    < 5m (1-2 lantai)<br>
                    Pajak: 1.0x<br>
                    Jumlah: {height_distribution['Rendah']}
                </div>
                <div style='padding: 10px; background: #fef9c3; border-left: 4px solid #eab308; border-radius: 5px;'>
                    <b>🏘️ Sedang</b><br>
                    5-10m (2-3 lantai)<br>
                    Pajak: 1.3x<br>
                    Jumlah: {height_distribution['Sedang']}
                </div>
                <div style='padding: 10px; background: #fed7aa; border-left: 4px solid #f97316; border-radius: 5px;'>
                    <b>🏢 Tinggi</b><br>
                    10-15m (3-5 lantai)<br>
                    Pajak: 1.6x<br>
                    Jumlah: {height_distribution['Tinggi']}
                </div>
                <div style='padding: 10px; background: #fecaca; border-left: 4px solid #ef4444; border-radius: 5px;'>
                    <b>🏬 Gedung</b><br>
                    > 15m (5+ lantai)<br>
                    Pajak: 2.0x<br>
                    Jumlah: {height_distribution['Gedung']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.info("""
        **💡 Cara Menggunakan:**
        
        1. **Zoom In/Out**: Scroll mouse
        2. **Pan**: Drag peta
        3. **Klik Bangunan**: Lihat detail lengkap
        4. **Hover**: Lihat info singkat
        
        Warna kotak = tinggi bangunan
        """)
    
    components.html(m._repr_html_(), height=750)
    
    st.success("✅ Demo mode dengan visualisasi tinggi bangunan interaktif aktif!")
    
    if st.button("🔄 Coba Mode Real"):
        st.session_state['demo_mode'] = False
        st.rerun()
    
    st.stop()

# --- REAL MODE ---
auth_success = initialize_gee()

if not auth_success:
    st.stop()

# Real GEE Logic with client-side rendering
try:
    with st.spinner("🔄 Memuat data bangunan dari satelit..."):
        # Expand ROI to cover larger area (3x radius for maximum coverage)
        coverage_multiplier = 3 if load_all else 2
        roi = ee.Geometry.Point([116.1165, -8.5831]).buffer(inspector_radius * coverage_multiplier)
        
        # Load DSM datasets for all modes (will only be used if needed)
        dsm = None
        dtm = None
        
        # Check if we need DSM data
        use_dsm_method = height_method in ["DSM (Digital Surface Model)", "Hybrid (Cepat + Akurat)"]
        
        if use_dsm_method:
            st.info("📡 Memuat data Digital Surface Model (ALOS World 3D)...")
            try:
                # ALOS World 3D - 30m resolution DSM
                dsm = ee.Image("JAXA/ALOS/AW3D30/V3_2").select('DSM')
                
                # FABDEM - Filtered DEM (acts as DTM - ground level)
                dtm = ee.Image("PROJECTS/sat-io/open-datasets/FABDEM").select('b1')
            except Exception as e:
                st.warning(f"⚠️ Gagal memuat DSM: {e}. Akan menggunakan estimasi untuk semua bangunan.")
                use_dsm_method = False
        
        # Buildings Dataset
        buildings_dataset = ee.FeatureCollection("GOOGLE/Research/open-buildings/v3/polygons")
        buildings_filtered = buildings_dataset.filterBounds(roi).limit(max_buildings)
        
        # Try to get building data
        try:
            # Get features as list
            features = buildings_filtered.getInfo()['features']
            
            if len(features) >= max_buildings:
                st.warning(f"⚠️ Menampilkan {len(features)} bangunan (limit tercapai). Tingkatkan 'Max Buildings to Load' di sidebar untuk melihat lebih banyak.")
            else:
                st.success(f"✅ Berhasil memuat {len(features)} bangunan dari Google Earth Engine!")
            
            # Create map with Google Satellite
            m = folium.Map(
                location=MATARAM_COORDS,
                zoom_start=initial_zoom,
                max_zoom=21,
                tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
                attr='Google Satellite'
            )
            
            total_area = 0
            total_tax = 0
            height_distribution = {'Rendah': 0, 'Sedang': 0, 'Tinggi': 0, 'Gedung': 0}
            dsm_count = 0
            est_count = 0
            
            # Progress bar for DSM processing
            if use_dsm_method:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Pre-filter buildings that need DSM
                if height_method == "Hybrid (Cepat + Akurat)":
                    large_buildings = [f for f in features if f['properties'].get('area_in_meters', 0) > dsm_threshold]
                    status_text.text(f"🚀 Mode Hybrid: {len(large_buildings)}/{len(features)} bangunan akan pakai DSM (bangunan > {dsm_threshold}m²)")
                else:
                    large_buildings = features
                    status_text.text(f"📡 Mode DSM Penuh: Semua {len(features)} bangunan akan pakai DSM")
            
            # Data for charts and export
            processed_data = []
            
            # Render each building
            for idx, feature in enumerate(features):
                # Update progress
                if use_dsm_method and idx % 20 == 0:
                    progress = (idx + 1) / len(features)
                    progress_bar.progress(progress)
                    status_text.text(f"Memproses bangunan {idx + 1}/{len(features)}...")
                
                props = feature['properties']
                geom = feature['geometry']
                
                # Get building properties
                area = props.get('area_in_meters', 100)
                height = None
                method_used = ""
                
                # Filter by Area early if possible (though we need coords for DSM)
                if area < filter_min_area or area > filter_max_area:
                    continue
                
                # Get coordinates first
                if geom['type'] == 'Polygon':
                    coords = geom['coordinates'][0]
                    # Convert from [lon, lat] to [lat, lon] for Folium
                    folium_coords = [[c[1], c[0]] for c in coords]
                    
                    # Calculate centroid
                    avg_lat = sum(c[0] for c in folium_coords) / len(folium_coords)
                    avg_lon = sum(c[1] for c in folium_coords) / len(folium_coords)
                    
                    # Decide whether to use DSM based on method and building size
                    should_use_dsm = False
                    if height_method == "DSM (Digital Surface Model)":
                        should_use_dsm = True
                    elif height_method == "Hybrid (Cepat + Akurat)":
                        should_use_dsm = (area > dsm_threshold)
                    
                    # Try DSM method if applicable and DSM data is available
                    if should_use_dsm and dsm is not None and dtm is not None:
                        ee_geometry = ee.Geometry.Polygon(coords)
                        dsm_height = get_building_height_from_dsm(ee_geometry, dsm, dtm)
                        
                        if dsm_height and dsm_height > 0.5:
                            height = dsm_height
                            method_used = "DSM"
                            dsm_count += 1
                    
                    # Fallback to estimation if DSM not used or failed
                    if height is None or height < 0.5:
                        height = estimate_height_from_area(area)
                        method_used = "Estimasi"
                        est_count += 1
                    
                    height_info = classify_height(height)
                    
                    # Filter by Category
                    if height_info['category'] not in filter_category:
                        continue
                        
                    building_data = {
                        'lat': avg_lat,
                        'lon': avg_lon,
                        'area': area,
                        'height': height,
                        'category': height_info['category'],
                        'method': method_used
                    }
                    
                    tax_mult = height_info['multiplier'] * height_tax_multiplier
                    tax = area * tax_rate * tax_mult
                    
                    building_data['tax'] = tax
                    processed_data.append(building_data)
                    
                    height_distribution[height_info['category']] += 1
                    total_area += area
                    total_tax += tax
                    
                    # Add polygon with toggle support
                    if show_height_colors:
                        # Mode: Warna klasifikasi tinggi
                        polygon_color = height_info['color']
                        polygon_fill = True
                        polygon_fill_color = height_info['fill_color']
                        polygon_fill_opacity = 0.7
                    else:
                        # Mode: Outline merah saja
                        polygon_color = '#ff0000'
                        polygon_fill = False
                        polygon_fill_color = '#ff0000'
                        polygon_fill_opacity = 0
                    
                    folium.Polygon(
                        locations=folium_coords,
                        popup=folium.Popup(
                            create_building_popup(building_data, tax_rate, height_tax_multiplier, method_used),
                            max_width=300
                        ),
                        tooltip=f"{height_info['emoji']} {height_info['category']} - {height:.1f}m ({method_used}) - Klik untuk detail",
                        color=polygon_color,
                        fill=polygon_fill,
                        fillColor=polygon_fill_color,
                        fillOpacity=polygon_fill_opacity,
                        weight=2,
                        opacity=1
                    ).add_to(m)
            
            # Clear progress bar
            if use_dsm_method:
                progress_bar.empty()
                status_text.empty()
            
            # Add layer control
            folium.LayerControl().add_to(m)
            
            with tab_map:
                # Display metrics for current view
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("🏢 Bangunan Terfilter", len(processed_data))
                col2.metric("📏 Total Area", f"{int(total_area):,} m²")
                col3.metric("📐 Rata-rata Tinggi", f"{total_area / len(processed_data) if len(processed_data) > 0 else 0:.1f} m")
                col4.metric("💰 Potensi Pajak", f"Rp {int(total_tax):,}")
                
                # Height legend
                if show_height_colors:
                    st.markdown(f"""
                    <div class="height-legend">
                        <b style='font-size: 16px;'>🏢 Distribusi Tinggi Bangunan ({height_method}):</b><br><br>
                        <div style='display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px;'>
                            <div style='text-align: center; padding: 10px; background: #dcfce7; border-radius: 5px;'>
                                <div style='font-size: 24px;'>🏠</div>
                                <b>Rendah</b><br>
                                {height_distribution['Rendah']} bangunan
                            </div>
                            <div style='text-align: center; padding: 10px; background: #fef9c3; border-radius: 5px;'>
                                <div style='font-size: 24px;'>🏘️</div>
                                <b>Sedang</b><br>
                                {height_distribution['Sedang']} bangunan
                            </div>
                            <div style='text-align: center; padding: 10px; background: #fed7aa; border-radius: 5px;'>
                                <div style='font-size: 24px;'>🏢</div>
                                <b>Tinggi</b><br>
                                {height_distribution['Tinggi']} bangunan
                            </div>
                            <div style='text-align: center; padding: 10px; background: #fecaca; border-radius: 5px;'>
                                <div style='font-size: 24px;'>🏬</div>
                                <b>Gedung</b><br>
                                {height_distribution['Gedung']} bangunan
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                components.html(m._repr_html_(), height=750)
                
                st.info(f"""
                💡 **Tips:**
                - Zoom in untuk melihat detail bentuk bangunan
                - Klik bangunan untuk info lengkap (badge menunjukkan metode: DSM atau EST)
                - Centang "🚀 Muat SEMUA Bangunan" untuk coverage maksimal
                
                📐 **Metode {height_method}:**
                {'- 🚀 Hybrid: DSM untuk bangunan besar (>'+str(dsm_threshold)+'m²), estimasi untuk kecil' if height_method == "Hybrid (Cepat + Akurat)" else ''}
                {'- Menggunakan ALOS World 3D (resolusi 30m)' if 'DSM' in height_method or 'Hybrid' in height_method else ''}
                {'- Lebih cepat dari DSM penuh, lebih akurat dari estimasi penuh' if height_method == "Hybrid (Cepat + Akurat)" else ''}
                {'- Akurasi: ±2-3 meter untuk bangunan besar' if 'DSM' in height_method or 'Hybrid' in height_method else ''}
                """)

            with tab_stats:
                if not processed_data:
                    st.warning("⚠️ Tidak ada data untuk dianalisis. Sesuaikan filter Anda.")
                else:
                    import pandas as pd
                    import plotly.express as px
                    import plotly.graph_objects as go
                    
                    df = pd.DataFrame(processed_data)
                    
                    st.header("📊 Analisis Data Bangunan Terfilter")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Pie chart categories
                        fig_pie = px.pie(df, names='category', title='Distribusi Kategori Bangunan',
                                        color='category',
                                        color_discrete_map={
                                            'Rendah': '#22c55e',
                                            'Sedang': '#eab308',
                                            'Tinggi': '#f97316',
                                            'Gedung': '#ef4444'
                                        })
                        st.plotly_chart(fig_pie, use_container_width=True)
                    
                    with col2:
                        # Bar chart area vs tax
                        fig_bar = px.bar(df.groupby('category')['tax'].sum().reset_index(), 
                                        x='category', y='tax', title='Total Potensi Pajak per Kategori',
                                        color='category',
                                        color_discrete_map={
                                            'Rendah': '#22c55e',
                                            'Sedang': '#eab308',
                                            'Tinggi': '#f97316',
                                            'Gedung': '#ef4444'
                                        })
                        st.plotly_chart(fig_bar, use_container_width=True)
                    
                    # Area vs Height Scatter
                    fig_scatter = px.scatter(df, x='area', y='height', color='category',
                                            title='Korelasi Luas Area vs Tinggi Bangunan',
                                            hover_data=['method', 'tax'])
                    st.plotly_chart(fig_scatter, use_container_width=True)
                    
                    # Data Table
                    st.subheader("📋 Daftar Bangunan")
                    st.dataframe(df[['category', 'area', 'height', 'tax', 'method', 'lat', 'lon']], use_container_width=True)
                    
                    # Export Button
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Data (CSV)",
                        data=csv,
                        file_name='mataram_building_tax_report.csv',
                        mime='text/csv',
                    )
            
            
        except Exception as e:
            st.error(f"Error saat memuat data bangunan: {e}")
            st.info("Coba kurangi 'Max Buildings to Load' atau gunakan Demo Mode untuk visualisasi.")
            
except Exception as e:
    st.error(f"Map Rendering Error: {e}")
    st.info("Coba refresh halaman atau gunakan Demo Mode.")
