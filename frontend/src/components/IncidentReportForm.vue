<template>
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

      <form @submit.prevent="handleSubmit" class="space-y-4">
        <!-- Severity (Krusial) -->
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

        <!-- Location -->
        <div class="space-y-2">
          <Label for="location" class="text-sm font-semibold">Location <span class="text-red-500">*</span></Label>
          <Select v-model="formData.location">
            <SelectTrigger class="w-full">
              <SelectValue placeholder="Select location" />
            </SelectTrigger>
            <SelectContent>
              <SelectGroup>
                <SelectItem v-for="location in locations" :key="location.id" :value="location.id">
                  {{ location.name }}
                </SelectItem>
              </SelectGroup>
            </SelectContent>
          </Select>
        </div>

        <!-- Description -->
        <div class="space-y-2">
          <Label for="description" class="text-sm font-semibold">Description <span class="text-red-500">*</span></Label>
          <Textarea
            v-model="formData.description"
            placeholder="Describe the incident in detail..."
            class="min-h-[100px]"
          />
        </div>

        <!-- Proof/Evidence Image -->
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
              <img :src="imagePreview" class="max-h-[150px] mx-auto rounded" />
              <p class="text-sm text-slate-600">{{ formData.proof_image.name }}</p>
              <button type="button" @click.stop="removeImage" class="text-xs text-red-600 hover:text-red-700">Remove</button>
            </div>
          </div>
        </div>

        <!-- Employee Involved -->
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
        </div>

        <!-- Impact Preview -->
        <div class="bg-slate-50 p-4 rounded-lg border border-slate-200">
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

        <DialogFooter>
          <Button type="button" variant="outline" @click="$emit('update:open', false)">Cancel</Button>
          <Button type="submit" :disabled="!formData.severity || !formData.location || !formData.description || !formData.proof_image || isSubmitting">
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

const formData = ref({
  severity: '',
  location: '',
  description: '',
  employee_name: '',
  proof_image: null,
  reported_by: props.empId,
  vessel_id: authState.selectedVessel?.asset_id || authState.assignedVessel?.asset_id || ''
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
    const response = await fetch(`${API_BASE_URL}/hse/employees/`, {
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
    // Fetch from HSE POB module with vessel filter
    const response = await fetch(`${API_BASE_URL}/hse/pob/work-locations/?vessel_id=${vesselId}`, {
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

watch(() => props.open, (newVal) => {
  if (newVal) {
    fetchEmployees();
    fetchLocations();
  }
});

// Watch for vessel changes and re-fetch locations
watch(() => authState.selectedVessel?.asset_id || authState.assignedVessel?.asset_id, (newVesselId) => {
  if (newVesselId) {
    formData.value.vessel_id = newVesselId;
    fetchLocations();
  }
});

const handleSubmit = async () => {
  if (!formData.value.severity || !formData.value.location || !formData.value.description || !formData.value.proof_image) {
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

    // Add vessel_id to ensure incident is linked to correct vessel
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

      // Emit event untuk update dashboard
      emit('incident-reported', data);

      // Reset form
      formData.value = {
        severity: '',
        location: '',
        description: '',
        employee_name: '',
        proof_image: null,
        reported_by: props.empId,
        vessel_id: authState.selectedVessel?.asset_id || authState.assignedVessel?.asset_id || ''
      };

      if (fileInput.value) {
        fileInput.value.value = '';
      }

      emit('update:open', false);
    } else {
      const error = await response.json();
      toast.error("Failed", { description: error.detail || "Failed to report incident" });
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

      // Reset form
      formData.value = {
        severity: '',
        location: '',
        description: '',
        employee_name: '',
        proof_image: null,
        reported_by: props.empId,
        vessel_id: authState.selectedVessel?.asset_id || authState.assignedVessel?.asset_id || ''
      };
      if (fileInput.value) {
        fileInput.value.value = '';
      }
      
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
