import ee
import streamlit as st
import os

def initialize_gee():
    """
    Initializes Google Earth Engine with comprehensive fallback strategies.
    """
    # Strategy 0: Check for Streamlit Secrets (Cloud Deployment)
    if "gee_service_account" in st.secrets:
        try:
            service_account = st.secrets["gee_service_account"]
            # Convert string to dict if needed (secrets usually return parsed toml/json)
            # If standard service account JSON structure
            credentials = ee.ServiceAccountCredentials(
                service_account['client_email'], 
                key_data=str(service_account).replace("'", '"') # minimal handle
            )
            # Actually, standard way for st.secrets with private key is:
            # ee.Initialize(credentials=...) is harder without a key file.
            # Easier way: standard gcloud auth application-default logic using environment variable?
            # Or use ee.Initialize with service account. 
            # To allow easy deployment, we'll try PROJECT_ID from secrets first.
            
            # Correct way to use service account in Streamlit Cloud
            project_id = service_account["project_id"]
            ee.Initialize(credentials=credentials, project=project_id)
            st.success(f"✅ Connected via Streamlit Secrets (Project: {project_id})")
            return True
        except Exception as e:
            st.warning(f"⚠️ Secrets found but auth failed: {e}")

    # Strategy 1: Try standard initialization
    try:
        ee.Initialize(project="mataram-sstb")
        st.success("✅ Connected to Google Earth Engine!")
        return True
    except Exception as e1:
        error_msg = str(e1)
        
        # Strategy 2: Check if it's a "no project" error
        if "project" in error_msg.lower():
            st.warning("⚠️ GEE authenticated but no default project found.")
            
            # Try to find credentials file and extract project
            cred_path = os.path.expanduser("~/.config/earthengine/credentials")
            if os.path.exists(cred_path):
                try:
                    import json
                    with open(cred_path, 'r') as f:
                        creds = json.load(f)
                        if 'project_id' in creds or 'project' in creds:
                            project = creds.get('project_id') or creds.get('project')
                            ee.Initialize(project=project)
                            st.success(f"✅ Connected using project: {project}")
                            return True
                except:
                    pass
            
            # Strategy 3: Try with common project patterns
            st.info("🔄 Attempting alternative initialization...")
            try:
                # This forces a re-check of credentials
                ee.Initialize(opt_url='https://earthengine.googleapis.com')
                st.success("✅ Connected via alternative method!")
                return True
            except Exception as e3:
                pass

        
        # Strategy 4: Show helpful error and demo mode option
        st.error(f"❌ GEE Initialization Failed: {error_msg}")
        
        with st.expander("🔧 Troubleshooting Steps"):
            st.markdown("""
            **Masalah:** Google Earth Engine tidak dapat menemukan Cloud Project Anda.
            
            **Solusi Manual:**
            1. Buka [Google Cloud Console](https://console.cloud.google.com)
            2. Buat project baru (misal: `mataram-sstb`)
            3. Catat nama project tersebut
            4. Edit file `utils.py` baris 12, ganti menjadi:
               ```python
               ee.Initialize(project='mataram-sstb')  # Ganti dengan nama project Anda
               ```
            5. Restart aplikasi
            """)
        
        # Offer demo mode
        if st.button("🎮 Launch Demo Mode (Offline Simulation)", key="demo_btn"):
            st.session_state['demo_mode'] = True
            st.rerun()
        
        return False
