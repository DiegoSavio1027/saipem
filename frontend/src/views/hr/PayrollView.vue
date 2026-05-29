<template>
  <DashboardLayout>
    <div class="p-8">
      <!-- Header -->
      <div class="flex flex-col md:flex-row justify-between items-start md:items-end gap-4 mb-8 no-print">
        <div>
          <h2 class="text-3xl font-black text-slate-900 dark:text-white tracking-tight uppercase">Automated Payroll</h2>
          <p class="text-xs text-slate-500 dark:text-slate-600 uppercase tracking-wider mt-1">Real-time offshore compensation & allowance calculator engine</p>
        </div>

        <!-- Month/Year Selector -->
        <div class="flex items-center gap-3 bg-white dark:bg-slate-900 p-2 rounded-xl border border-slate-200 dark:border-slate-800">
          <select v-model="selectedMonth" @change="loadPayroll" class="bg-slate-50 dark:bg-black border border-slate-200 dark:border-slate-800 text-slate-900 dark:text-white text-xs py-2.5 px-4 rounded-lg font-bold uppercase focus:border-[var(--color-saipem-tertiary)] outline-none transition cursor-pointer">
            <option v-for="(month, index) in months" :key="index" :value="index + 1">{{ month }}</option>
          </select>
          <select v-model="selectedYear" @change="loadPayroll" class="bg-slate-50 dark:bg-black border border-slate-200 dark:border-slate-800 text-slate-900 dark:text-white text-xs py-2.5 px-4 rounded-lg font-bold focus:border-[var(--color-saipem-tertiary)] outline-none transition cursor-pointer">
            <option value="2026">2026</option>
            <option value="2027">2027</option>
          </select>
        </div>
      </div>

      <!-- Main Content Grid -->
      <div class="grid grid-cols-1 xl:grid-cols-3 gap-6 items-start">
        <!-- Pay Ledger Table -->
        <div class="xl:col-span-2 bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden no-print">
          <div class="p-5 border-b border-slate-200 dark:border-slate-800/80 bg-slate-50 dark:bg-slate-950/40">
            <h3 class="text-sm font-black uppercase tracking-wider text-slate-900 dark:text-white">Personnel Pay Ledger</h3>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse table-fixed">
              <thead>
                <tr class="bg-slate-50 dark:bg-slate-950 border-b border-slate-200 dark:border-slate-800 text-slate-500 dark:text-slate-600 font-bold text-xs uppercase tracking-widest">
                  <th class="p-4 border-r border-slate-200 dark:border-slate-900 w-24">ID</th>
                  <th class="p-4 border-r border-slate-200 dark:border-slate-900 w-48">Name</th>
                  <th class="p-4 border-r border-slate-200 dark:border-slate-900 w-24 text-center">Days Onboard</th>
                  <th class="p-4 border-r border-slate-200 dark:border-slate-900 w-36 text-right">Standard Rate</th>
                  <th class="p-4 border-r border-slate-200 dark:border-slate-900 w-40 text-right">Net Earnings</th>
                  <th class="p-4 text-center w-24">Action</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-200 dark:divide-slate-800/60 font-medium text-xs">
                <tr v-if="loading" class="hover:bg-slate-50 dark:hover:bg-slate-900/40 transition duration-150">
                  <td colspan="6" class="p-8 text-center text-slate-500 dark:text-slate-600">
                    <Loader class="w-6 h-6 animate-spin text-[var(--color-saipem-tertiary)] mb-2 mx-auto" />
                    <p class="font-mono text-xs uppercase tracking-widest mt-2">Re-calculating ledger entries...</p>
                  </td>
                </tr>
                <tr v-else-if="payrollRecords.length === 0" class="hover:bg-slate-50 dark:hover:bg-slate-900/40 transition duration-150">
                  <td colspan="6" class="p-8 text-center text-slate-500 dark:text-slate-600 font-mono text-xs uppercase tracking-widest">NO PERSONNEL ROSTERED ON THIS PERIOD.</td>
                </tr>
                <tr v-for="rec in payrollRecords" :key="rec.emp_id" class="hover:bg-slate-50 dark:hover:bg-slate-900/40 transition duration-150">
                  <td class="p-4 font-mono text-[var(--color-saipem-tertiary)] border-r border-slate-200 dark:border-slate-900">{{ rec.emp_id }}</td>
                  <td class="p-4 font-bold text-slate-900 dark:text-white truncate border-r border-slate-200 dark:border-slate-900">{{ rec.full_name }}</td>
                  <td class="p-4 text-center font-mono font-bold border-r border-slate-200 dark:border-slate-900" :class="rec.total_days > 0 ? 'text-orange-600 dark:text-orange-400' : 'text-slate-500 dark:text-slate-600'">{{ rec.total_days }} Days</td>
                  <td class="p-4 text-right font-mono border-r border-slate-200 dark:border-slate-900 text-slate-600 dark:text-slate-500">Rp {{ formatCurrency(rec.daily_rate) }}</td>
                  <td class="p-4 text-right font-mono font-bold border-r border-slate-200 dark:border-slate-900 text-slate-900 dark:text-white">Rp {{ formatCurrency(rec.total_earnings) }}</td>
                  <td class="p-4 text-center">
                    <button @click="generateSlip(rec.emp_id)" class="bg-orange-100 dark:bg-orange-950/20 hover:bg-orange-200 dark:hover:bg-orange-950/40 border border-orange-200 dark:border-orange-500/20 hover:border-orange-400 dark:hover:border-orange-500 text-orange-700 dark:text-orange-400 font-bold px-3 py-1.5 rounded-lg text-xs tracking-widest uppercase transition-all">
                      View Slip
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Payslip Panel -->
        <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm p-6 text-slate-900 dark:text-white">
          <div class="text-center py-6 border-b border-slate-200 dark:border-slate-800/80 border-dashed">
            <div class="bg-orange-100 dark:bg-orange-950/20 w-16 h-16 rounded-full border border-orange-200 dark:border-orange-500/30 flex items-center justify-center mx-auto mb-3 text-[var(--color-saipem-tertiary)]">
              <Receipt class="w-8 h-8 animate-pulse" />
            </div>
            <h3 class="text-md font-black uppercase tracking-widest text-slate-900 dark:text-white">Offshore Pay Slip</h3>
            <p class="text-xs text-slate-500 dark:text-slate-600 uppercase tracking-widest mt-1">SAIPEM PAYSLIP ENGINE</p>
          </div>

          <div v-if="!selectedPayslip" class="p-4 text-center text-slate-500 dark:text-slate-600 text-xs py-16">
            Select a crew member to generate secure pay slip receipt.
          </div>

          <div v-else class="space-y-5 pt-6">
            <!-- Employee Info -->
            <div class="space-y-1 font-mono text-xs uppercase tracking-widest text-slate-600 dark:text-slate-500">
              <div class="flex justify-between"><span>SPM FILE:</span><span class="text-slate-900 dark:text-white">{{ selectedPayslip.emp_id }}</span></div>
              <div class="flex justify-between"><span>BENEFICIARY:</span><span class="text-slate-900 dark:text-white truncate max-w-[150px]">{{ selectedPayslip.full_name }}</span></div>
              <div class="flex justify-between"><span>DESIGNATION:</span><span class="text-slate-900 dark:text-white">{{ selectedPayslip.job_role }}</span></div>
              <div class="flex justify-between"><span>PAY PERIOD:</span><span class="text-[var(--color-saipem-tertiary)] font-bold">{{ monthName }} {{ selectedYear }}</span></div>
            </div>

            <!-- Compensation Breakdown -->
            <div class="border-t border-slate-200 dark:border-slate-800/80 border-dashed pt-4 space-y-3 font-mono text-xs uppercase tracking-widest">
              <h4 class="font-black text-slate-900 dark:text-white text-sm mb-2">Compensation Breakdown</h4>
              <div class="flex justify-between">
                <span>Base Day Rate:</span>
                <span class="text-slate-600 dark:text-slate-400">Rp {{ formatCurrency(selectedPayslip.daily_rate) }}</span>
              </div>
              <div class="flex justify-between border-b border-slate-200 dark:border-slate-800 pb-2 mb-2">
                <span>Onboard Duration:</span>
                <span class="text-[var(--color-saipem-tertiary)] font-bold">{{ selectedPayslip.total_days }} Onboard Days</span>
              </div>
              <div class="flex justify-between text-slate-900 dark:text-white font-bold">
                <span>Total Base Pay:</span>
                <span>Rp {{ formatCurrency(selectedPayslip.base_pay) }}</span>
              </div>
            </div>

            <!-- Allowances -->
            <div class="border-t border-slate-200 dark:border-slate-800/80 border-dashed pt-4 space-y-3 font-mono text-xs uppercase tracking-widest">
              <h4 class="font-black text-slate-900 dark:text-white text-sm mb-2">Allowances</h4>
              <div class="flex justify-between">
                <span>Offshore Allowance Rate:</span>
                <span class="text-slate-600 dark:text-slate-400">Rp {{ formatCurrency(selectedPayslip.allowance_rate) }} / Day</span>
              </div>
              <div class="flex justify-between text-slate-900 dark:text-white font-bold">
                <span>Total Allowance:</span>
                <span>Rp {{ formatCurrency(selectedPayslip.allowance_pay) }}</span>
              </div>
            </div>

            <!-- Net Remittance -->
            <div class="border-t border-slate-200 dark:border-slate-800/80 border-dashed pt-4 flex justify-between items-center">
              <div class="font-black text-slate-600 dark:text-slate-500 text-xs tracking-widest uppercase">Net Remittance</div>
              <div class="text-right">
                <div class="text-lg font-black text-green-600 dark:text-green-400 font-mono">Rp {{ formatCurrency(selectedPayslip.total_earnings) }}</div>
                <div class="text-xs text-slate-500 dark:text-slate-600 font-mono">FIT FOR TRANSACTION</div>
              </div>
            </div>

            <!-- Print Button -->
            <button @click="printPayslip" class="w-full bg-[var(--color-saipem-tertiary)] hover:bg-orange-600 text-white font-black py-3 rounded-xl transition tracking-wider uppercase flex items-center justify-center gap-2 mt-4 text-xs no-print">
              <Printer class="w-4 h-4" /> Print Payslip Receipt
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Print-Only Section -->
    <div id="payslip-print" class="hidden print:block print:p-0 print:m-0">
      <div v-if="selectedPayslip" class="w-full max-w-2xl mx-auto p-8 bg-white text-slate-900">
        <div class="text-center py-6 border-b border-slate-300 border-dashed mb-6">
          <h3 class="text-lg font-black uppercase tracking-widest">Offshore Pay Slip</h3>
          <p class="text-xs text-slate-600 uppercase tracking-widest mt-1">SAIPEM PAYSLIP ENGINE</p>
        </div>

        <!-- Employee Info -->
        <div class="space-y-1 font-mono text-xs uppercase tracking-widest text-slate-700 mb-6">
          <div class="flex justify-between"><span>SPM FILE:</span><span class="font-bold">{{ selectedPayslip.emp_id }}</span></div>
          <div class="flex justify-between"><span>BENEFICIARY:</span><span class="font-bold">{{ selectedPayslip.full_name }}</span></div>
          <div class="flex justify-between"><span>DESIGNATION:</span><span class="font-bold">{{ selectedPayslip.job_role }}</span></div>
          <div class="flex justify-between"><span>PAY PERIOD:</span><span class="font-bold">{{ monthName }} {{ selectedYear }}</span></div>
        </div>

        <!-- Compensation Breakdown -->
        <div class="border-t border-slate-300 border-dashed pt-4 space-y-2 font-mono text-xs uppercase tracking-widest mb-6">
          <h4 class="font-black text-slate-900 text-sm mb-3">Compensation Breakdown</h4>
          <div class="flex justify-between">
            <span>Base Day Rate:</span>
            <span>Rp {{ formatCurrency(selectedPayslip.daily_rate) }}</span>
          </div>
          <div class="flex justify-between border-b border-slate-300 pb-2 mb-2">
            <span>Onboard Duration:</span>
            <span class="font-bold">{{ selectedPayslip.total_days }} Onboard Days</span>
          </div>
          <div class="flex justify-between font-bold">
            <span>Total Base Pay:</span>
            <span>Rp {{ formatCurrency(selectedPayslip.base_pay) }}</span>
          </div>
        </div>

        <!-- Allowances -->
        <div class="border-t border-slate-300 border-dashed pt-4 space-y-2 font-mono text-xs uppercase tracking-widest mb-6">
          <h4 class="font-black text-slate-900 text-sm mb-3">Allowances</h4>
          <div class="flex justify-between">
            <span>Offshore Allowance Rate:</span>
            <span>Rp {{ formatCurrency(selectedPayslip.allowance_rate) }} / Day</span>
          </div>
          <div class="flex justify-between font-bold">
            <span>Total Allowance:</span>
            <span>Rp {{ formatCurrency(selectedPayslip.allowance_pay) }}</span>
          </div>
        </div>

        <!-- Net Remittance -->
        <div class="border-t border-slate-300 border-dashed pt-4 flex justify-between items-center">
          <div class="font-black text-slate-700 text-xs tracking-widest uppercase">Net Remittance</div>
          <div class="text-right">
            <div class="text-lg font-black text-green-600 font-mono">Rp {{ formatCurrency(selectedPayslip.total_earnings) }}</div>
            <div class="text-xs text-slate-600 font-mono">FIT FOR TRANSACTION</div>
          </div>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { authState } from '@/store/auth'
import DashboardLayout from '@/layouts/DashboardLayout.vue'
import { Loader, Receipt, Printer } from '@lucide/vue'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1'

// Data
const payrollRecords = ref([])
const selectedPayslip = ref(null)
const loading = ref(false)

// UI State
const selectedMonth = ref(new Date().getMonth() + 1)
const selectedYear = ref(new Date().getFullYear().toString())

const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

// Computed
const monthName = computed(() => months[selectedMonth.value - 1])

// Methods
const formatCurrency = (value) => {
  return new Intl.NumberFormat('id-ID').format(value || 0)
}

const loadPayroll = async () => {
  loading.value = true
  selectedPayslip.value = null
  try {
    const response = await fetch(`${API_BASE_URL}/hr/payroll/?month=${selectedMonth.value}&year=${selectedYear.value}`)
    if (response.ok) {
      payrollRecords.value = await response.json()
    } else {
      payrollRecords.value = []
    }
  } catch (err) {
    console.error('Error loading payroll:', err)
    payrollRecords.value = []
  } finally {
    loading.value = false
  }
}

const generateSlip = (empId) => {
  selectedPayslip.value = payrollRecords.value.find(r => r.emp_id === empId)
}

const printPayslip = () => {
  window.print()
}

onMounted(() => {
  loadPayroll()
})
</script>

<style>
/* Global print styles - not scoped so it affects layout components */
@media print {
  /* Hide layout components */
  aside,
  nav,
  header,
  footer,
  .sidebar,
  .topbar,
  .mobile-header,
  .mobile-bottom-nav {
    display: none !important;
  }

  /* Hide the main content wrapper but keep main visible */
  .flex.h-screen {
    display: block !important;
    height: auto !important;
  }

  .flex.flex-col.flex-1 {
    display: block !important;
  }

  main {
    padding: 0 !important;
    margin: 0 !important;
  }

  /* Show only the print section */
  #payslip-print {
    display: block !important;
    visibility: visible !important;
  }

  /* Hide everything else in main */
  main > div:not(#payslip-print) {
    display: none !important;
  }
}
</style>

<style scoped>
#payslip-print {
  display: none;
}

@media print {
  /* Reset everything */
  * {
    margin: 0 !important;
    padding: 0 !important;
    background: white !important;
    color: black !important;
    box-shadow: none !important;
  }

  /* Show the print section */
  #payslip-print {
    display: block !important;
    visibility: visible !important;
    position: static !important;
    width: 100% !important;
    height: auto !important;
  }

  #payslip-print * {
    visibility: visible !important;
  }

  /* Text colors for print */
  .text-slate-900,
  .text-slate-700,
  .text-slate-600 {
    color: #000 !important;
  }

  .text-green-600 {
    color: #059669 !important;
  }

  .border-slate-300 {
    border-color: #999 !important;
  }

  /* Ensure flex displays work */
  .flex {
    display: flex !important;
  }

  .justify-between {
    justify-content: space-between !important;
  }

  .items-center {
    align-items: center !important;
  }

  .text-center {
    text-align: center !important;
  }

  .text-right {
    text-align: right !important;
  }
}
</style>
