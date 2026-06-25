import sys

content = """<template>
  <Dialog :open="open" @update:open="$emit('update:open', $event)">
    <DialogContent class="max-w-2xl">
      <DialogHeader>
        <DialogTitle>Report Incident</DialogTitle>
        <DialogDescription>
          {{ authState.userRole === 'Worker'
            ? 'Report a safety observation to help maintain a safe work environment'
            : 'Report an incident to update safety metrics and system status' }}
        </DialogDescription>
      </DialogHeader>

      <!-- Step Indicators -->
      <div class="flex items-center justify-between mt-4 mb-8 relative">
        <div class="absolute left-0 top-1/2 -translate-y-1/2 w-full h-1 bg-slate-200 dark:bg-slate-700 z-0 rounded-full"></div>
        <div 
          class="absolute left-0 top-1/2 -translate-y-1/2 h-1 bg-blue-500 z-0 rounded-full transition-all duration-300"
          :style="{ width: ((currentStep - 1) / 2) * 100 + '%' }"
        ></div>
        
        <div v-for="stepNum in 3" :key="stepNum" class="relative z-10 flex flex-col items-center gap-2">
          <div 
            class="w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm border-2 transition-colors duration-300"
            :class="[
              currentStep === stepNum ? 'bg-blue-600 border-blue-600 text-white' :
              currentStep > stepNum ? 'bg-blue-500 border-blue-500 text-white' : 'bg-white dark:bg-slate-800 border-slate-300 text-slate-400'
            ]"
          >
            <span v-if="currentStep > stepNum">✓</span>
            <span v-else>{{ stepNum }}</span>
          </div>
          <span 
            class="text-xs font-medium absolute -bottom-6 w-24 text-center"
            :class="currentStep >= stepNum ? 'text-slate-900 dark:text-slate-100' : 'text-slate-400'"
          >
            {{ stepNames[stepNum - 1] }}
          </span>
        </div>
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-4 pt-4">
        <!-- Step 1: Classification -->
        <div v-if="currentStep === 1" class="space-y-4 animate-in fade-in slide-in-from-right-4 duration-300">
          <div class="space-y-2">
            <Label for="severity" class="text-sm font-semibold">Incident Type / Severity <span class="text-red-500">*</span></Label>
            <Select v-model="formData.severity">
              <SelectTrigger class="w-full">
                <SelectValue placeholder="Select severity level" />
              </SelectTrigger>
              <SelectContent>
                <SelectGroup>
                  <SelectItem value="SAFETY_OBSERVATION">
                    <span class="flex items-center gap-2">
                      <span class="w-2 h-2 rounded-full bg-blue-500"></span>
                      Safety Observation
                    </span>
                  </SelectItem>
                  <SelectItem value="NEAR_MISS">
                    <span class="flex items-center gap-2">
                      <span class="w-2 h-2 rounded-full bg-yellow-500"></span>
                      Near Miss
                    </span>
                  </SelectItem>
                  <SelectItem value="FIRST_AID">
                    <span class="flex items-center gap-2">
                      <span class="w-2 h-2 rounded-full bg-orange-500"></span>
                      First Aid / Minor Injury
                    </span>
                  </SelectItem>
                  <SelectItem value="LTI">
                    <span class="flex items-center gap-2">
                      <span class="w-2 h-2 rounded-full bg-red-500"></span>
                      LTI / Major Injury
                    </span>
                  </SelectItem>
                </SelectGroup>
              </SelectContent>
            </Select>
            <p v-if="authState.userRole === 'Worker'" class="text-xs text-blue-600 dark:text-blue-400">ℹ️ All reports will be verified by Safety Officer before affecting metrics</p>
            <p v-else class="text-xs text-slate-500">⭐ This selection will automatically update metrics and system status</p>
          </div>

          <div class="space-y-2">
            <Label for="description" class="text-sm font-semibold">Description <span class="text-red-500">*</span></Label>
            <Textarea
              v-model="formData.description"
              placeholder="Describe the incident in detail..."
              class="min-h-[120px]"
            />
          </div>
        </div>

        <!-- Step 2: Where & Who -->
        <div v-if="currentStep === 2" class="space-y-4 animate-in fade-in slide-in-from-right-4 duration-300">
          <div class="space-y-2">
            <Label for="location" class="text-sm font-semibold">Location (Deck) <span class="text-red-500">*</span></Label>
            <Select v-model="formData.location">
              <SelectTrigger class="w-full">
                <SelectValue placeholder="Select location" />
              </SelectTrigger>
              <SelectContent>
                <SelectGroup>
                  <SelectItem v-for="location in locations" :key="location.id" :value="location.id">
                    {{ location.deck_name || location.name }}
                  </SelectItem>
                </SelectGroup>
              </SelectContent>
            </Select>
          </div>

          <div class="space-y-2">
            <Label for="employee" class="text-sm font-semibold">Employee Involved</Label>
            <Select v-model="formData.employee_name">
              <SelectTrigger class="w-full">
                <SelectValue placeholder="Select employee (if any)" />
              </SelectTrigger>
              <SelectContent>
                <SelectGroup>
                  <SelectItem v-for="employee in employees" :key="employee.emp_id" :value="employee.full_name">
                    {{ employee.full_name }}
                  </SelectItem>
                </SelectGroup>
              </SelectContent>
            </Select>
            <p class="text-xs text-slate-500">List is filtered by current active vessel roster.</p>
          </div>
        </div>

        <!-- Step 3: Evidence & Impact Preview -->
        <div v-if="currentStep === 3" class="space-y-4 animate-in fade-in slide-in-from-right-4 duration-300">
          <div class="space-y-2">
            <Label for="proof_image" class="text-sm font-semibold">Proof/Evidence Image <span class="text-red-500">*</span></Label>
            <div class="border-2 border-dashed border-slate-300 rounded-lg p-4 text-center cursor-pointer hover:border-slate-400 transition-colors" @click="$refs.fileInput.click()">
              <input
                ref="fileInput"
                type="file"
                accept="image/*"
                class="hidden"
                @change="handleImageUpload"
              />
              <div v-if="!formData.proof_image" class="space-y-2">
                <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mx-auto text-slate-400">
                  <rect width="18" height="18" x="3" y="3" rx="2" ry="2"/>
                  <circle cx="8.5" cy="8.5" r="1.5"/>
                  <path d="m21 15-5-5L7 22"/>
                </svg>
                <p class="text-sm text-slate-600">Click to upload image or drag and drop</p>
                <p class="text-xs text-slate-500">PNG, JPG, GIF up to 5MB</p>
              </div>
              <div v-else class="space-y-2">
                <img :src="imagePreview" class="max-h-[150px] mx-auto rounded object-contain" />
                <p class="text-sm font-medium text-slate-700">{{ formData.proof_image.name }}</p>
                <button type="button" @click.stop="removeImage" class="text-xs text-red-600 hover:text-red-700 font-semibold px-2 py-1 bg-red-50 rounded-md">Remove Image</button>
              </div>
            </div>
          </div>

          <div class="bg-slate-50 p-4 rounded-lg border border-slate-200 mt-4">
            <p class="text-sm font-semibold text-slate-900 mb-3">System Impact Preview:</p>
            <div class="space-y-2 text-sm">
              <div v-if="formData.severity === 'SAFETY_OBSERVATION'" class="space-y-1">
                <p class="text-slate-700">✓ <strong>Near Misses:</strong> No change</p>
                <p class="text-slate-700">✓ <strong>Days Without LTI:</strong> No change</p>
                <p class="text-slate-700">✓ <strong>Condition Status:</strong> Remain GREEN 🟢</p>
                <p class="text-slate-500 text-xs mt-2">Minor hazard observation only, no impact on metrics</p>
              </div>
              <div v-else-if="formData.severity === 'NEAR_MISS'" class="space-y-1">
                <p class="text-slate-700">✓ <strong>Near Misses:</strong> +1</p>
                <p class="text-slate-700">✓ <strong>Days Without LTI:</strong> No change</p>
                <p class="text-slate-700">✓ <strong>Condition Status:</strong> Remain GREEN 🟢</p>
                <p class="text-slate-500 text-xs mt-2">Close call but no actual accident occurred</p>
              </div>
              <div v-else-if="formData.severity === 'FIRST_AID'" class="space-y-1">
                <p class="text-slate-700">✓ <strong>Near Misses:</strong> No change</p>
                <p class="text-slate-700">✓ <strong>Days Without LTI:</strong> No change</p>
                <p class="text-amber-600">⚠️ <strong>Condition Status:</strong> May change to YELLOW ⚠️</p>
                <p class="text-slate-500 text-xs mt-2">Minor injury treated with first aid</p>
              </div>
              <div v-else-if="formData.severity === 'LTI'" class="space-y-1">
                <p class="text-red-600">🚨 <strong>Days Without LTI:</strong> Reset to 0 days</p>
                <p class="text-slate-700">✓ <strong>Near Misses:</strong> No change</p>
                <p class="text-red-600">🚨 <strong>Condition Status:</strong> AUTO → RED 🔴</p>
                <p class="text-red-600 text-xs mt-2 font-semibold">⚠️ SYSTEM WILL ACTIVATE EMERGENCY MODE!</p>
                <p class="text-red-600 text-xs">- Ship alarm will sound</p>
                <p class="text-red-600 text-xs">- New PTW approvals frozen</p>
                <p class="text-red-600 text-xs">- Evacuation protocols ready</p>
              </div>
            </div>
          </div>
        </div>

        <DialogFooter class="pt-6 sm:justify-between flex-row">
          <Button 
            type="button" 
            variant="outline" 
            @click="currentStep === 1 ? $emit('update:open', false) : currentStep--"
          >
            {{ currentStep === 1 ? 'Cancel' : 'Back' }}
          </Button>
          
          <Button 
            v-if="currentStep < 3" 
            type="button" 
            class="bg-blue-600 hover:bg-blue-700"
            :disabled="!canProceed" 
            @click="currentStep++"
          >
            Next Step
          </Button>
          
          <Button 
            v-if="currentStep === 3" 
            type="submit" 
            class="bg-green-600 hover:bg-green-700"
            :disabled="!canSubmit || isSubmitting"
          >
            {{ isSubmitting ? 'Submitting...' : 'Submit Report' }}
          </Button>
        </DialogFooter>
      </form>
    </DialogContent>
  </Dialog>
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectGroup, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { toast } from 'vue-sonner';
import { getCsrfToken } from '@/utils/csrf';
import { authState, getAccessToken } from '@/store/auth';
import { addToQueue, fileToBase64 } from '@/utils/offlineSync';

const props = defineProps({
  open: Boolean,
  empId: String
});

const emit = defineEmits(['update:open', 'incident-reported']);

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1';
const isSubmitting = ref(false);
const employees = ref([]);
const locations = ref([]);
const fileInput = ref(null);

const currentStep = ref(1);
const stepNames = ['Classification', 'Location', 'Evidence'];

const formData = ref({
  severity: '',
  location: '',
  description: '',
  employee_name: '',
  proof_image: null,
  reported_by: props.empId,
  vessel_id: authState.selectedVessel?.asset_id || authState.assignedVessel?.asset_id || ''
});

const canProceed = computed(() => {
  if (currentStep.value === 1) {
    return formData.value.severity && formData.value.description;
  }
  if (currentStep.value === 2) {
    return formData.value.location !== '';
  }
  return true;
});

const canSubmit = computed(() => {
  return formData.value.severity && 
         formData.value.description && 
         formData.value.location !== '' && 
         formData.value.proof_image;
});

const imagePreview = computed(() => {
  if (formData.value.proof_image) {
    return URL.createObjectURL(formData.value.proof_image);
  }
  return null;
});

const handleImageUpload = (event) => {
  const file = event.target.files?.[0];
  if (file) {
    if (file.size > 5 * 1024 * 1024) {
      toast.error("Error", { description: "Image size must be less than 5MB" });
      return;
    }
    formData.value.proof_image = file;
  }
};

const removeImage = () => {
  formData.value.proof_image = null;
  if (fileInput.value) {
    fileInput.value.value = '';
  }
};

const fetchEmployees = async () => {
  try {
    const vesselId = authState.selectedVessel?.asset_id || authState.assignedVessel?.asset_id;
    let url = `${API_BASE_URL}/hr/employees/`;
    if (vesselId) {
      url += `?vessel_id=${vesselId}`;
    }
    
    const response = await fetch(url, {
      headers: {
        'Authorization': `Bearer ${getAccessToken()}`
      }
    });
    if (response.ok) {
      const data = await response.json();
      employees.value = data;
    }
  } catch (error) {
    console.error("Failed to fetch employees:", error);
  }
};

const fetchLocations = async () => {
  try {
    const vesselId = authState.selectedVessel?.asset_id || authState.assignedVessel?.asset_id;
    if (!vesselId) {
      console.warn('No vessel assigned. Cannot fetch locations.');
      locations.value = [];
      return;
    }
    // Fetch from offshore module with vessel filter
    const response = await fetch(`${API_BASE_URL}/offshore/locations/?vessel_id=${vesselId}`, {
      headers: {
        'Authorization': `Bearer ${getAccessToken()}`
      }
    });
    if (response.ok) {
      const data = await response.json();
      locations.value = data;
    }
  } catch (error) {
    console.error("Failed to fetch locations:", error);
  }
};

const resetForm = () => {
  formData.value = {
    severity: '',
    location: '',
    description: '',
    employee_name: '',
    proof_image: null,
    reported_by: props.empId,
    vessel_id: authState.selectedVessel?.asset_id || authState.assignedVessel?.asset_id || ''
  };
  currentStep.value = 1;
  if (fileInput.value) {
    fileInput.value.value = '';
  }
};

watch(() => props.open, (newVal) => {
  if (newVal) {
    currentStep.value = 1;
    formData.value.vessel_id = authState.selectedVessel?.asset_id || authState.assignedVessel?.asset_id || '';
    fetchEmployees();
    fetchLocations();
  } else {
    resetForm();
  }
});

// Watch for vessel changes and re-fetch locations
watch(() => authState.selectedVessel?.asset_id || authState.assignedVessel?.asset_id, (newVesselId) => {
  if (newVesselId) {
    formData.value.vessel_id = newVesselId;
    if (props.open) {
      fetchLocations();
      fetchEmployees();
    }
  }
});

const handleSubmit = async () => {
  if (!canSubmit.value) {
    toast.error("Error", { description: "Please fill all required fields including proof image" });
    return;
  }

  isSubmitting.value = true;
  try {
    const formDataToSend = new FormData();
    formDataToSend.append('severity', formData.value.severity);
    formDataToSend.append('location', formData.value.location);
    formDataToSend.append('description', formData.value.description);
    formDataToSend.append('reported_by', formData.value.reported_by);
    formDataToSend.append('incident_date', new Date().toISOString());

    if (formData.value.employee_name) {
      formDataToSend.append('employee_name', formData.value.employee_name);
    }

    if (formData.value.vessel_id) {
      formDataToSend.append('vessel_id', formData.value.vessel_id);
    }

    if (formData.value.proof_image) {
      formDataToSend.append('proof_image', formData.value.proof_image);
    }

    const response = await fetch(`${API_BASE_URL}/hse/incidents/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCsrfToken() || '',
        'Authorization': `Bearer ${getAccessToken()}`
      },
      body: formDataToSend
    });

    if (response.ok) {
      const data = await response.json();
      toast.success("Incident Reported", {
        description: `Incident reported successfully. System status updated.`
      });

      emit('incident-reported', data);
      emit('update:open', false);
    } else {
      const error = await response.json();
      console.error("Backend error:", error);
      toast.error("Failed", { description: error.detail || "Failed to report incident. Check server logs." });
    }
  } catch (error) {
    console.error("Error reporting incident, attempting to queue offline:", error);
    
    try {
      const base64Image = await fileToBase64(formData.value.proof_image);
      const payload = {
        severity: formData.value.severity,
        location: formData.value.location,
        description: formData.value.description,
        reported_by: formData.value.reported_by,
        incident_date: new Date().toISOString(),
        employee_name: formData.value.employee_name || '',
        vessel_id: formData.value.vessel_id || '',
        proof_image_base64: base64Image,
        proof_image_name: formData.value.proof_image.name,
        proof_image_type: formData.value.proof_image.type
      };

      addToQueue('INCIDENT_CREATE', `${API_BASE_URL}/hse/incidents/`, payload, {
        'X-CSRFToken': getCsrfToken() || '',
        'Authorization': `Bearer ${getAccessToken()}`
      });
      
      toast.info("Saved Offline", { description: "Incident queued for sync when online." });
      emit('incident-reported', { offline: true });
      emit('update:open', false);
    } catch (err) {
      console.error("Failed to queue offline incident:", err);
      toast.error("Error", { description: "Failed to queue incident report locally." });
    }
  } finally {
    isSubmitting.value = false;
  }
};
</script>
"""

with open("/Users/septiandwica/Documents/President University/saipem-hse/frontend/src/components/IncidentReportForm.vue", "w") as f:
    f.write(content)
