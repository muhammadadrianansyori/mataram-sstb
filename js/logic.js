/**
 * Form Logic Module
 */

const Logic = {
    /**
     * Determines which sections should be visible based on structure type
     * @param {string} structureType - The selected structure type value
     * @returns {object} - Object containing visibility states
     */
    getSectionVisibility(structureType) {
        // Core Logic: "If 'Canopy' is selected, skip to Documentation..."
        // Also skip for "False Positive/Artifact" as it implies no building exists
        
        const isPermanent = structureType === 'permanent';
        
        return {
            dimensionalAnalysis: isPermanent
        };
    },

    /**
     * Generates mock metadata for the prototype
     * @returns {object} - Mock data
     */
    generateMockMetadata() {
        const today = new Date();
        const randomDays = Math.floor(Math.random() * 10);
        const detectionDate = new Date(today);
        detectionDate.setDate(today.getDate() - randomDays);

        return {
            referenceId: `REF-${Math.floor(Math.random() * 90000) + 10000}-SAT`,
            timestamp: detectionDate.toISOString().split('T')[0] + ' ' + detectionDate.toTimeString().split(' ')[0]
        };
    },

    /**
     * Form Validation
     * @param {FormData} formData 
     */
    validate(formData) {
        const errors = [];
        const structureType = formData.get('structureType');

        if (!structureType) {
            errors.push("Structure Type is required.");
        }

        if (structureType === 'permanent') {
            const area = formData.get('footprintArea');
            if (!area || area <= 0) {
                errors.push("Valid Footprint Area is required for permanent buildings.");
            }
        }

        return errors;
    }
};

// Expose to global scope for app.js
window.Logic = Logic;
