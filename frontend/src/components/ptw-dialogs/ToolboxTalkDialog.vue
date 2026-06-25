<template>
  <Dialog :open="open" @update:open="$emit('update:open', $event)">
    <DialogContent class="sm:max-w-[550px] max-h-[90vh] overflow-y-auto">
      <DialogHeader>
        <DialogTitle>Pre-Job Safety Verification (JSA/TBT)</DialogTitle>
        <DialogDescription>
          Permit ID: <span class="font-bold text-[var(--color-saipem-tertiary)]">{{ permitId }}</span>
        </DialogDescription>
      </DialogHeader>

      <!-- Step Indicators -->
      <div class="flex items-center justify-between border-b border-slate-200 dark:border-slate-700 pb-4 mb-4">
        <div v-for="stepNum in 3" :key="stepNum" class="flex items-center">
          <div :class="[
            'w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm transition-colors',
            currentStep === stepNum ? 'bg-[var(--color-saipem-tertiary)] text-white' :
            currentStep > stepNum ? 'bg-green-500 text-white' : 'bg-slate-200 dark:bg-slate-800 text-slate-500'
          ]">
            <span v-if="currentStep > stepNum">✓</span>
            <span v-else>{{ stepNum }}</span>
          </div>
          <span :class="[
            'ml-2 text-xs font-semibold hidden sm:inline',
            currentStep === stepNum ? 'text-slate-900 dark:text-slate-100' : 'text-slate-400'
          ]">
            {{ stepNames[stepNum - 1] }}
          </span>
          <div v-if="stepNum < 3" class="w-8 sm:w-16 h-0.5 mx-2 bg-slate-200 dark:bg-slate-700"></div>
        </div>
      </div>

      <!-- Step 1: JSA PPE Checklist -->
      <div v-if="currentStep === 1" class="space-y-4 py-2">
        <h3 class="text-sm font-semibold text-slate-800 dark:text-slate-200">1. Job Safety Analysis (JSA) Checklist</h3>
        <p class="text-xs text-slate-500">Confirm the required Personal Protective Equipment (PPE) is inspected and available for use:</p>
        
        <div class="grid grid-cols-2 gap-3 bg-slate-50 dark:bg-slate-900 p-4 rounded-lg border border-slate-200 dark:border-slate-800">
          <div v-for="(label, key) in ppeItems" :key="key" class="flex items-center space-x-3 py-1">
            <Checkbox :id="key" v-model="jsaData.ppeChecked[key]" />
            <Label :for="key" class="text-xs font-medium cursor-pointer">{{ label }}</Label>
          </div>
        </div>
        <p class="text-[10px] text-red-500 font-semibold" v-if="currentStep === 1 && (!jsaData.ppeChecked.helmet || !jsaData.ppeChecked.boots || !jsaData.ppeChecked.gloves)">
            * You must verify that at least Safety Helmet, Steel-Toe Boots, and Work Gloves are available to proceed.
        </p>

        <div class="flex items-start space-x-3 p-3 bg-amber-50 dark:bg-amber-950/20 rounded-lg border border-amber-200 dark:border-amber-900/50">
          <Checkbox id="loto" v-model="jsaData.lotoApplied" />
          <div class="grid gap-1">
            <Label for="loto" class="text-xs font-semibold text-amber-900 dark:text-amber-400 cursor-pointer">Lockout / Tagout (LOTO) Applied</Label>
            <p class="text-[10px] text-amber-700 dark:text-amber-500">Check this if the job requires equipment energy isolation and LOTO devices have been secured.</p>
          </div>
        </div>
      </div>

      <!-- Step 2: Photo & Attendance -->
      <div v-if="currentStep === 2" class="space-y-4 py-2">
        <h3 class="text-sm font-semibold text-slate-800 dark:text-slate-200">2. Toolbox Talk (TBT) Attendance & Photo</h3>
        
        <!-- Photo Upload -->
        <div class="space-y-2">
          <Label class="text-xs font-semibold">TBT Briefing Proof (Photo) <span class="text-red-500">*</span></Label>
          <div class="border-2 border-dashed border-slate-350 dark:border-slate-700 rounded-lg p-4 text-center cursor-pointer hover:border-slate-400 transition-colors" @click="$refs.fileInput.click()">
            <input ref="fileInput" type="file" accept="image/*" class="hidden" @change="handlePhotoChange" />
            <div v-if="!tbtPhotoBase64" class="space-y-1">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mx-auto text-slate-450"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
              <p class="text-xs text-slate-600 font-medium">Click to upload crew TBT photo</p>
              <p class="text-[10px] text-slate-400">JPEG/PNG format up to 5MB</p>
            </div>
            <div v-else class="space-y-2">
              <img :src="tbtPhotoBase64" class="max-h-[120px] mx-auto rounded border" />
              <button type="button" @click.stop="tbtPhotoBase64 = ''" class="text-[10px] text-red-600 font-semibold hover:underline">Remove Image</button>
            </div>
          </div>
        </div>

        <!-- Attendance List -->
        <div class="space-y-2">
          <Label class="text-xs font-semibold">Confirm Attendees Present <span class="text-red-500">*</span></Label>
          <div class="border border-slate-200 dark:border-slate-800 rounded-lg max-h-[150px] overflow-y-auto divide-y dark:divide-slate-800">
            <!-- Applicant -->
            <div class="flex items-center justify-between p-2.5">
              <span class="text-xs font-medium text-slate-800 dark:text-slate-200">{{ applicantName }} (Applicant)</span>
              <span class="text-[10px] bg-green-150 text-green-700 px-2 py-0.5 rounded-full font-bold">Present</span>
            </div>
            <!-- Crew members -->
            <div v-for="member in crewList" :key="member.emp_id" class="flex items-center justify-between p-2.5">
              <span class="text-xs text-slate-800 dark:text-slate-200">{{ member.full_name }} (Crew)</span>
              <Checkbox :id="'att-' + member.emp_id" v-model="attendance[member.emp_id]" />
            </div>
          </div>
        </div>
      </div>

      <!-- Step 3: Digital Sign-off -->
      <div v-if="currentStep === 3" class="space-y-4 py-2">
        <h3 class="text-sm font-semibold text-slate-800 dark:text-slate-200">3. Attendance Signature Sign-off</h3>
        <p class="text-xs text-slate-500">Each present crew member must type their name to sign off on safety declarations:</p>

        <div class="space-y-3 max-h-[220px] overflow-y-auto pr-1">
          <!-- Applicant signature -->
          <div class="p-3 border rounded-lg bg-slate-50 dark:bg-slate-900 border-slate-200 dark:border-slate-800 space-y-2">
            <Label :for="'sig-' + ptw?.emp_id" class="text-xs font-bold text-slate-700 dark:text-slate-350">{{ applicantName }} (Applicant)</Label>
            <input :id="'sig-' + ptw?.emp_id" type="text" v-model="signatures[ptw?.emp_id || '']" placeholder="Type name to sign" class="w-full text-xs p-2 border rounded dark:bg-slate-800 dark:border-slate-700" />
          </div>
          <!-- Crew signatures (only if selected as present) -->
          <div v-for="member in presentCrew" :key="member.emp_id" class="p-3 border rounded-lg bg-slate-50 dark:bg-slate-900 border-slate-200 dark:border-slate-800 space-y-2">
            <Label :for="'sig-' + member.emp_id" class="text-xs font-bold text-slate-700 dark:text-slate-350">{{ member.full_name }} (Crew)</Label>
            <input :id="'sig-' + member.emp_id" type="text" v-model="signatures[member.emp_id]" placeholder="Type name to sign" class="w-full text-xs p-2 border rounded dark:bg-slate-800 dark:border-slate-700" />
          </div>
        </div>

        <div class="flex items-start space-x-3 p-3 bg-blue-50 dark:bg-blue-950/20 rounded-lg border border-blue-200 dark:border-blue-900/50">
          <Checkbox id="tbt-declared" v-model="tbtDeclared" />
          <Label for="tbt-declared" class="text-[10px] leading-tight text-blue-900 dark:text-blue-400 font-semibold cursor-pointer">
            We declare that we have attended the Toolbox Talk briefing, understood the identified hazards, and commit to following safe work protocols.
          </Label>
        </div>
      </div>

      <!-- Navigation & Actions -->
      <DialogFooter class="flex items-center justify-between border-t border-slate-200 dark:border-slate-700 pt-4 mt-4">
        <Button type="button" variant="outline" :disabled="currentStep === 1" @click="currentStep--">
          Back
        </Button>
        <div class="flex gap-2">
          <Button type="button" variant="outline" @click="$emit('update:open', false)">
            Cancel
          </Button>
          <Button v-if="currentStep < 3" type="button" :disabled="!canProceed" @click="currentStep++">
            Next
          </Button>
          <Button v-else type="button" :disabled="!canSubmit" @click="handleConfirm">
            Confirm & Start Work
          </Button>
        </div>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { Label } from '@/components/ui/label';

const props = defineProps({
  open: Boolean,
  permitId: String,
  ptwId: Number,
  ptw: Object
});

const emit = defineEmits(['update:open', 'confirm']);

const currentStep = ref(1);
const stepNames = ['JSA PPE', 'Photo & Crew', 'Signatures'];

const ppeItems = {
  helmet: 'Safety Helmet / Hard Hat',
  boots: 'Safety Steel-Toe Boots',
  gloves: 'Protective Work Gloves',
  goggles: 'Safety Glasses / Goggles',
  harness: 'Full-Body Safety Harness',
  gasdetector: 'Portable Gas Detector'
};

// Form data refs
const jsaData = ref({
  ppeChecked: {
    helmet: false,
    boots: false,
    gloves: false,
    goggles: false,
    harness: false,
    gasdetector: false
  },
  lotoApplied: false
});

const tbtPhotoBase64 = ref('');
const attendance = ref({});
const signatures = ref({});
const tbtDeclared = ref(false);

const applicantName = computed(() => {
  return props.ptw?.employee?.full_name || props.ptw?.emp_id || 'Applicant';
});

const crewList = computed(() => {
  return props.ptw?.assigned_crew || [];
});

const presentCrew = computed(() => {
  return crewList.value.filter(member => attendance.value[member.emp_id] === true);
});

// Photo upload
const handlePhotoChange = (event) => {
  const file = event.target.files?.[0];
  if (file) {
    if (file.size > 5 * 1024 * 1024) {
      alert("Image size must be less than 5MB");
      return;
    }
    const reader = new FileReader();
    reader.onload = (e) => {
      tbtPhotoBase64.value = e.target.result;
    };
    reader.readAsDataURL(file);
  }
};

// Wizard validations
const canProceed = computed(() => {
  if (currentStep.value === 1) {
    // Require at least basic PPE checked (helmet, boots, gloves)
    const ppe = jsaData.value.ppeChecked;
    return ppe.helmet && ppe.boots && ppe.gloves;
  }
  if (currentStep.value === 2) {
    // Require TBT Photo proof
    return !!tbtPhotoBase64.value;
  }
  return true;
});

const canSubmit = computed(() => {
  if (!tbtDeclared.value) return false;
  // Require signature from applicant
  if (!signatures.value[props.ptw?.emp_id || '']?.trim()) return false;
  // Require signature from all present crew
  for (const crew of presentCrew.value) {
    if (!signatures.value[crew.emp_id]?.trim()) {
      return false;
    }
  }
  return true;
});

// Watch open to reset form
watch(() => props.open, (isOpen) => {
  if (isOpen) {
    currentStep.value = 1;
    jsaData.value = {
      ppeChecked: {
        helmet: false,
        boots: false,
        gloves: false,
        goggles: false,
        harness: false,
        gasdetector: false
      },
      lotoApplied: false
    };
    tbtPhotoBase64.value = '';
    tbtDeclared.value = false;

    // Reset attendance
    const initialAttendance = {};
    const initialSignatures = {};
    
    // Applicant
    if (props.ptw?.emp_id) {
      initialSignatures[props.ptw.emp_id] = '';
    }

    // Crew
    crewList.value.forEach(member => {
      initialAttendance[member.emp_id] = true; // Present by default
      initialSignatures[member.emp_id] = '';
    });
    
    attendance.value = initialAttendance;
    signatures.value = initialSignatures;
  }
});

const handleConfirm = () => {
  // Build Checked PPE list
  const ppeCheckedList = Object.keys(jsaData.value.ppeChecked).filter(
    key => jsaData.value.ppeChecked[key] === true
  );

  // Build Signature JSON list
  const signatureList = [];
  // Applicant signature
  signatureList.push({
    emp_id: props.ptw?.emp_id,
    full_name: applicantName.value,
    role: 'Applicant',
    signature_name: signatures.value[props.ptw?.emp_id || '']
  });
  // Crew signatures
  presentCrew.value.forEach(crew => {
    signatureList.push({
      emp_id: crew.emp_id,
      full_name: crew.full_name,
      role: 'Crew',
      signature_name: signatures.value[crew.emp_id]
    });
  });

  const payload = {
    ptwId: props.ptwId,
    jsa_ppe_checked: ppeCheckedList,
    jsa_loto_applied: jsaData.value.lotoApplied,
    tbt_photo: tbtPhotoBase64.value,
    tbt_signatures: signatureList
  };

  emit('confirm', payload);
  emit('update:open', false);
};
</script>
