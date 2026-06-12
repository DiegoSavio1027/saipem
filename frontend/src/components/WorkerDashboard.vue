<template>
  <div class="space-y-6">
    <!-- Worker Profile Header -->
    <div class="bg-white dark:bg-slate-800 p-6 rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
      <div class="flex items-center gap-4">
        <div class="w-16 h-16 rounded-xl bg-orange-100 dark:bg-orange-950/40 text-[var(--color-saipem-tertiary)] flex items-center justify-center font-bold text-2xl border border-orange-200 dark:border-orange-900/50">
          {{ userInitial }}
        </div>
        <div>
          <div class="flex items-center gap-2 flex-wrap">
            <h2 class="text-2xl font-bold text-slate-900 dark:text-slate-100">
              {{ employeeDetail?.full_name || authState.username }}
            </h2>
            <span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400">
              <span class="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse"></span>
              Live POB: Onboard
            </span>
          </div>
          <p class="text-sm text-slate-500 dark:text-slate-400 mt-1">
            {{ employeeDetail?.job_role || 'Offshore Crew' }} • {{ employeeDetail?.email || '-' }}
          </p>
        </div>
      </div>
      <button @click="$emit('open-submit-modal')" class="w-full md:w-auto bg-[var(--color-saipem-tertiary)] hover:bg-[var(--color-saipem-tertiary)]/90 text-white px-6 py-3 rounded-lg font-semibold text-sm transition-colors shadow-md hover:shadow-lg flex items-center justify-center gap-2">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="M12 5v14"/></svg>
        Submit New PTW
      </button>
    </div>

    <!-- Quick KPI Stats Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <!-- Roster Card -->
      <Card class="hover:shadow-md transition-shadow">
        <CardContent class="p-6 flex items-start gap-4">
          <div class="p-3 rounded-lg bg-blue-50 dark:bg-blue-950/30 text-blue-600 dark:text-blue-400">
            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/><path d="m9 16 2 2 4-4"/></svg>
          </div>
          <div>
            <p class="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Active Roster</p>
            <h4 class="text-lg font-bold text-slate-900 dark:text-slate-100 mt-1">
              {{ activeRoster ? activeRoster.vessel_name : 'No Active Roster' }}
            </h4>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-1 font-medium">
              {{ remainingDays }} days remaining onboard
            </p>
          </div>
        </CardContent>
      </Card>

      <!-- MCU Fitness Card -->
      <Card class="hover:shadow-md transition-shadow">
        <CardContent class="p-6 flex items-start gap-4">
          <div :class="[
            'p-3 rounded-lg',
            employeeDetail?.mcu_status === 'FIT' ? 'bg-green-50 dark:bg-green-950/30 text-green-600 dark:text-green-400' : 'bg-red-50 dark:bg-red-950/30 text-red-600 dark:text-red-400'
          ]">
            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>
          </div>
          <div>
            <p class="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">MCU Status</p>
            <h4 class="text-lg font-bold text-slate-900 dark:text-slate-100 mt-1 flex items-center gap-2">
              {{ employeeDetail?.mcu_status || 'PENDING' }}
              <span :class="[
                'w-2 h-2 rounded-full',
                employeeDetail?.mcu_status === 'FIT' ? 'bg-green-500' : 'bg-red-500'
              ]"></span>
            </h4>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">
              Expires: {{ formatDate(employeeDetail?.mcu_expiry) }}
            </p>
          </div>
        </CardContent>
      </Card>

      <!-- Estimated Payroll Card -->
      <Card class="hover:shadow-md transition-shadow">
        <CardContent class="p-6 flex items-start gap-4">
          <div class="p-3 rounded-lg bg-orange-50 dark:bg-orange-950/30 text-[var(--color-saipem-tertiary)]">
            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="12" x="2" y="6" rx="2"/><circle cx="12" cy="12" r="2"/><path d="M6 12h.01M18 12h.01"/></svg>
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Est. Monthly Salary</p>
            <h4 class="text-lg font-bold text-slate-900 dark:text-slate-100 mt-1 truncate">
              {{ formatRupiah(myPayroll?.total_earnings) || 'Calculating...' }}
            </h4>
            <button @click="showPayslipDialog = true" class="text-xs font-semibold text-[var(--color-saipem-tertiary)] hover:underline mt-1 block">
              View Pay Slip
            </button>
          </div>
        </CardContent>
      </Card>

      <!-- Active Permits Card -->
      <Card class="hover:shadow-md transition-shadow">
        <CardContent class="p-6 flex items-start gap-4">
          <div class="p-3 rounded-lg bg-purple-50 dark:bg-purple-950/30 text-purple-600 dark:text-purple-400">
            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" x2="8" y1="13" y2="13"/><line x1="16" x2="8" y1="17" y2="17"/></svg>
          </div>
          <div>
            <p class="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Active Permits</p>
            <h4 class="text-lg font-bold text-slate-900 dark:text-slate-100 mt-1">
              {{ activePermitsCount }} / {{ myPTWs.length }}
            </h4>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">
              {{ pendingPermitsCount }} awaiting approval
            </p>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Navigation Tabs -->
    <div class="border-b border-slate-200 dark:border-slate-700 flex gap-2 overflow-x-auto">
      <button
        @click="activeTab = 'permits'"
        :class="[
          'px-4 py-2.5 text-sm font-semibold border-b-2 transition-colors whitespace-nowrap',
          activeTab === 'permits'
            ? 'border-[var(--color-saipem-tertiary)] text-[var(--color-saipem-tertiary)]'
            : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300 dark:text-slate-400'
        ]"
      >
        Work Permits & affected Assets
      </button>
      <button
        @click="activeTab = 'roster'"
        :class="[
          'px-4 py-2.5 text-sm font-semibold border-b-2 transition-colors whitespace-nowrap',
          activeTab === 'roster'
            ? 'border-[var(--color-saipem-tertiary)] text-[var(--color-saipem-tertiary)]'
            : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300 dark:text-slate-400'
        ]"
      >
        My Roster & Location Schedule
      </button>
      <button
        @click="activeTab = 'payroll'"
        :class="[
          'px-4 py-2.5 text-sm font-semibold border-b-2 transition-colors whitespace-nowrap',
          activeTab === 'payroll'
            ? 'border-[var(--color-saipem-tertiary)] text-[var(--color-saipem-tertiary)]'
            : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300 dark:text-slate-400'
        ]"
      >
        Salary Rates & Pay Slips
      </button>
      <button
        @click="activeTab = 'certifications'"
        :class="[
          'px-4 py-2.5 text-sm font-semibold border-b-2 transition-colors whitespace-nowrap',
          activeTab === 'certifications'
            ? 'border-[var(--color-saipem-tertiary)] text-[var(--color-saipem-tertiary)]'
            : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300 dark:text-slate-400'
        ]"
      >
        Certifications & Training
      </button>
    </div>

    <!-- Tab Contents -->
    <div class="mt-6">
      <!-- 1. Permits Tab -->
      <div v-if="activeTab === 'permits'" class="grid grid-cols-1 xl:grid-cols-4 gap-6">
        <div class="xl:col-span-3">
          <Card>
            <CardHeader>
              <CardTitle>My Work Permits</CardTitle>
              <CardDescription>View, edit, or check-in to your work permits</CardDescription>
            </CardHeader>
            <CardContent>
              <DataTable
                title="My Work Permits"
                :data="myPTWs"
                :columns="columns"
              />
            </CardContent>
          </Card>
        </div>

        <!-- Affected Assets Widget -->
        <div class="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Affected Assets</CardTitle>
              <CardDescription>Machinery and units involved in your permits</CardDescription>
            </CardHeader>
            <CardContent>
              <div v-if="affectedAssets.length === 0" class="py-6 text-center text-sm text-slate-500 dark:text-slate-400">
                No active target assets on your permits.
              </div>
              <div v-else class="space-y-4">
                <div v-for="asset in affectedAssets" :key="asset.name" class="p-3 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg flex items-center justify-between">
                  <div class="flex items-center gap-3">
                    <div class="p-2 bg-orange-100 dark:bg-orange-950/20 text-[var(--color-saipem-tertiary)] rounded-md">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>
                    </div>
                    <div>
                      <h5 class="text-sm font-semibold text-slate-900 dark:text-slate-100">{{ asset.name }}</h5>
                      <p class="text-[11px] text-slate-500 dark:text-slate-400">Permits Active: {{ asset.permitsCount }}</p>
                    </div>
                  </div>
                  <span class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-semibold bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400 border border-blue-200 dark:border-blue-800">
                    {{ asset.latestPermitStatus }}
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card class="bg-gradient-to-br from-orange-50 to-orange-100/50 dark:from-orange-950/20 dark:to-orange-900/10 border-orange-200 dark:border-orange-900/40">
            <CardHeader class="pb-2">
              <CardTitle class="text-sm font-bold text-orange-900 dark:text-orange-400">Safety Notice</CardTitle>
            </CardHeader>
            <CardContent class="text-xs text-orange-800 dark:text-orange-300 leading-relaxed space-y-2">
              <p>1. Ensure you complete the **Toolbox Talk** before starting any work.</p>
              <p>2. Keep your personal check-in active. The Command Center tracks your live location for safety.</p>
              <p>3. Report any incident or asset malfunction immediately using the Topbar Test Alarm or Safety officer contact.</p>
            </CardContent>
          </Card>
        </div>
      </div>

      <!-- 2. Roster Tab -->
      <div v-if="activeTab === 'roster'" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2">
          <Card>
            <CardHeader>
              <CardTitle>My Deployment Roster History</CardTitle>
              <CardDescription>Your current and upcoming offshore rosters</CardDescription>
            </CardHeader>
            <CardContent>
              <div v-if="myRosters.length === 0" class="py-12 text-center text-sm text-slate-500">
                No roster entries found.
              </div>
              <div v-else class="space-y-4">
                <div v-for="roster in myRosters" :key="roster.id" class="p-4 border border-slate-200 dark:border-slate-700 rounded-lg bg-slate-50/50 dark:bg-slate-900/40">
                  <div class="flex justify-between items-start flex-wrap gap-2">
                    <div>
                      <h4 class="font-bold text-slate-900 dark:text-slate-100 text-base">
                        Vessel: {{ roster.vessel_name || roster.location }}
                      </h4>
                      <p class="text-sm text-slate-500 dark:text-slate-400 mt-1 flex items-center gap-1.5">
                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg>
                        Schedule: {{ formatDate(roster.start) }} - {{ formatDate(roster.end) }}
                      </p>
                      <p class="text-xs text-slate-400 dark:text-slate-500 mt-1">Location: {{ roster.location || 'Offshore Rig' }}</p>
                    </div>
                    <span :class="[
                      'px-2.5 py-1 rounded text-xs font-semibold',
                      isCurrentRoster(roster)
                        ? 'bg-green-100 text-green-700 dark:bg-green-950/30 dark:text-green-400 border border-green-200 dark:border-green-800'
                        : 'bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400'
                    ]">
                      {{ isCurrentRoster(roster) ? 'ACTIVE NOW' : 'SCHEDULED' }}
                    </span>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        <div>
          <Card>
            <CardHeader>
              <CardTitle>Vessel Activities</CardTitle>
              <CardDescription>Operations scheduled on {{ activeRoster?.vessel_name || 'your vessel' }}</CardDescription>
            </CardHeader>
            <CardContent>
              <div v-if="filteredActivities.length === 0" class="py-6 text-center text-sm text-slate-500 dark:text-slate-400">
                No current operations logged.
              </div>
              <div v-else class="space-y-4">
                <div v-for="act in filteredActivities" :key="act.id" class="p-3 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg">
                  <h5 class="text-sm font-bold text-slate-900 dark:text-slate-100">{{ act.activity_name }}</h5>
                  <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">
                    {{ formatDate(act.start) }} - {{ formatDate(act.end) }}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      <!-- 3. Payroll Tab -->
      <div v-if="activeTab === 'payroll'" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div>
          <Card>
            <CardHeader>
              <CardTitle>Salary Rate Configuration</CardTitle>
              <CardDescription>Your position rate details for {{ employeeDetail?.job_role }}</CardDescription>
            </CardHeader>
            <CardContent class="space-y-6">
              <div class="space-y-4">
                <div class="flex justify-between items-center py-2 border-b border-slate-100 dark:border-slate-800">
                  <span class="text-sm text-slate-500 dark:text-slate-400">Daily Base Rate</span>
                  <span class="font-bold text-slate-900 dark:text-slate-100">
                    {{ formatRupiah(myPayroll?.daily_rate) || 'Rp 500.000' }} / day
                  </span>
                </div>
                <div class="flex justify-between items-center py-2 border-b border-slate-100 dark:border-slate-800">
                  <span class="text-sm text-slate-500 dark:text-slate-400">Daily Offshore Allowance</span>
                  <span class="font-bold text-slate-900 dark:text-slate-100">
                    {{ formatRupiah(myPayroll?.allowance_rate) || 'Rp 300.000' }} / day
                  </span>
                </div>
                <div class="flex justify-between items-center py-2 border-b border-slate-100 dark:border-slate-800">
                  <span class="text-sm text-slate-500 dark:text-slate-400">Active Days Onboard (Current Month)</span>
                  <span class="font-bold text-slate-900 dark:text-slate-100">
                    {{ myPayroll?.total_days || 0 }} days
                  </span>
                </div>
              </div>

              <div class="p-4 bg-slate-50 dark:bg-slate-900/60 rounded-xl space-y-2">
                <div class="flex justify-between items-center text-xs text-slate-500">
                  <span>Gross Base Pay:</span>
                  <span>{{ formatRupiah((myPayroll?.daily_rate || 500000) * (myPayroll?.total_days || 0)) }}</span>
                </div>
                <div class="flex justify-between items-center text-xs text-slate-500">
                  <span>Allowance Pay:</span>
                  <span>{{ formatRupiah((myPayroll?.allowance_rate || 300000) * (myPayroll?.total_days || 0)) }}</span>
                </div>
                <div class="flex justify-between items-center text-sm font-bold text-slate-900 dark:text-slate-100 pt-2 border-t border-slate-200 dark:border-slate-800">
                  <span>Estimated Total:</span>
                  <span>{{ formatRupiah(myPayroll?.total_earnings) || 'Rp 0' }}</span>
                </div>
              </div>

              <button @click="showPayslipDialog = true" class="w-full bg-[var(--color-saipem-tertiary)] hover:bg-[var(--color-saipem-tertiary)]/90 text-white py-2.5 rounded-lg font-semibold text-sm transition-colors flex items-center justify-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" x2="8" y1="13" y2="13"/><line x1="16" x2="8" y1="17" y2="17"/></svg>
                View Printable Payslip
              </button>
            </CardContent>
          </Card>
        </div>

        <div class="lg:col-span-2">
          <Card class="h-full">
            <CardHeader>
              <CardTitle>Payroll History & Statements</CardTitle>
              <CardDescription>Access your previous payroll statements</CardDescription>
            </CardHeader>
            <CardContent>
              <div class="space-y-4">
                <!-- Mock Payroll Statements -->
                <div v-for="m in ['May 2026', 'April 2026', 'March 2026']" :key="m" class="p-4 border border-slate-100 dark:border-slate-800 bg-slate-50/20 dark:bg-slate-900/20 rounded-lg flex items-center justify-between">
                  <div>
                    <h5 class="font-bold text-slate-800 dark:text-slate-200 text-sm">Payslip Statement - {{ m }}</h5>
                    <p class="text-xs text-slate-400 dark:text-slate-500 mt-1">Status: Disbursed • Sent to Bank Account</p>
                  </div>
                  <button @click="showPayslipDialog = true" class="text-xs font-semibold px-3 py-1.5 rounded border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800">
                    Download
                  </button>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      <!-- 4. Certifications Tab -->
      <div v-if="activeTab === 'certifications'">
        <Card>
          <CardHeader>
            <CardTitle>My Certifications & Safety Cards</CardTitle>
            <CardDescription>Track certification validity required for hot work, height work, or confined space activities</CardDescription>
          </CardHeader>
          <CardContent>
            <div v-if="myCertifications.length === 0" class="py-12 text-center text-slate-500">
              No certifications logged in your profile. Please contact HR to register your certs.
            </div>
            <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div v-for="cert in myCertifications" :key="cert.cert_id" class="p-5 border border-slate-200 dark:border-slate-800 bg-slate-50/30 dark:bg-slate-900/30 rounded-xl relative overflow-hidden">
                <div class="flex justify-between items-start">
                  <div>
                    <span class="text-[10px] font-bold text-[var(--color-saipem-tertiary)] uppercase tracking-wider bg-orange-50 dark:bg-orange-950/20 px-2 py-0.5 rounded">
                      {{ cert.cert_type }}
                    </span>
                    <h4 class="font-bold text-slate-900 dark:text-slate-100 text-lg mt-2">{{ cert.cert_id }}</h4>
                    <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">
                      Expires: {{ formatDate(cert.expiry_date) }}
                    </p>
                  </div>
                  <span :class="[
                    'px-2 py-0.5 rounded text-[10px] font-bold',
                    isExpired(cert.expiry_date)
                      ? 'bg-red-100 text-red-700 dark:bg-red-950/30 dark:text-red-400 border border-red-200'
                      : 'bg-green-100 text-green-700 dark:bg-green-950/30 dark:text-green-400 border border-green-200'
                  ]">
                    {{ isExpired(cert.expiry_date) ? 'EXPIRED' : 'VALID' }}
                  </span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>

    <!-- Payslip Dialog -->
    <div v-if="showPayslipDialog" class="fixed inset-0 bg-slate-900/50 flex items-center justify-center p-4 z-50 overflow-y-auto">
      <div class="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 max-w-2xl w-full p-8 shadow-2xl relative">
        <button @click="showPayslipDialog = false" class="absolute top-4 right-4 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" x2="6" y1="6" y2="18"/><line x1="6" x2="18" y1="6" y2="18"/></svg>
        </button>

        <!-- Payslip Document -->
        <div id="print-payslip" class="space-y-6">
          <div class="flex justify-between items-start border-b border-slate-200 dark:border-slate-800 pb-4">
            <div>
              <h3 class="text-lg font-bold text-slate-900 dark:text-slate-100">SAIPEM OFFSHORE DIVISION</h3>
              <p class="text-xs text-slate-500">POB Roster Payroll Statement</p>
            </div>
            <div class="text-right">
              <span class="px-2 py-1 bg-slate-100 dark:bg-slate-800 text-[10px] font-bold rounded">CONFIDENTIAL</span>
              <p class="text-xs text-slate-500 mt-2">Date: {{ new Date().toLocaleDateString() }}</p>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4 text-sm">
            <div>
              <p class="text-slate-400 text-xs">Employee ID</p>
              <p class="font-semibold text-slate-900 dark:text-slate-100">{{ authState.username }}</p>
            </div>
            <div>
              <p class="text-slate-400 text-xs">Employee Name</p>
              <p class="font-semibold text-slate-900 dark:text-slate-100">{{ employeeDetail?.full_name || 'Offshore Worker' }}</p>
            </div>
            <div>
              <p class="text-slate-400 text-xs">Job Title</p>
              <p class="font-semibold text-slate-900 dark:text-slate-100">{{ employeeDetail?.job_role || 'Worker' }}</p>
            </div>
            <div>
              <p class="text-slate-400 text-xs">Assigned Vessel</p>
              <p class="font-semibold text-slate-900 dark:text-slate-100">{{ activeRoster?.vessel_name || '-' }}</p>
            </div>
          </div>

          <!-- Rates table -->
          <div class="border border-slate-200 dark:border-slate-800 rounded-lg overflow-hidden">
            <table class="w-full text-sm">
              <thead class="bg-slate-50 dark:bg-slate-800/50 border-b border-slate-200 dark:border-slate-800">
                <tr>
                  <th class="px-4 py-2 text-left font-semibold text-slate-500">Compensation Component</th>
                  <th class="px-4 py-2 text-center font-semibold text-slate-500">Days</th>
                  <th class="px-4 py-2 text-right font-semibold text-slate-500">Rate</th>
                  <th class="px-4 py-2 text-right font-semibold text-slate-500">Subtotal</th>
                </tr>
              </thead>
              <tbody>
                <tr class="border-b border-slate-100 dark:border-slate-800">
                  <td class="px-4 py-3 text-slate-800 dark:text-slate-300">Basic Daily Salary</td>
                  <td class="px-4 py-3 text-center text-slate-800 dark:text-slate-300">{{ myPayroll?.total_days || 0 }}</td>
                  <td class="px-4 py-3 text-right text-slate-800 dark:text-slate-300">{{ formatRupiah(myPayroll?.daily_rate) || 'Rp 500.000' }}</td>
                  <td class="px-4 py-3 text-right text-slate-800 dark:text-slate-300">
                    {{ formatRupiah((myPayroll?.daily_rate || 500000) * (myPayroll?.total_days || 0)) }}
                  </td>
                </tr>
                <tr class="border-b border-slate-100 dark:border-slate-800">
                  <td class="px-4 py-3 text-slate-800 dark:text-slate-300">Offshore Allowance</td>
                  <td class="px-4 py-3 text-center text-slate-800 dark:text-slate-300">{{ myPayroll?.total_days || 0 }}</td>
                  <td class="px-4 py-3 text-right text-slate-800 dark:text-slate-300">{{ formatRupiah(myPayroll?.allowance_rate) || 'Rp 300.000' }}</td>
                  <td class="px-4 py-3 text-right text-slate-800 dark:text-slate-300">
                    {{ formatRupiah((myPayroll?.allowance_rate || 300000) * (myPayroll?.total_days || 0)) }}
                  </td>
                </tr>
                <tr class="font-bold bg-slate-50 dark:bg-slate-800/30">
                  <td colspan="3" class="px-4 py-3 text-slate-900 dark:text-slate-100">Total Net Earnings</td>
                  <td class="px-4 py-3 text-right text-slate-900 dark:text-slate-100 text-base">
                    {{ formatRupiah(myPayroll?.total_earnings) || 'Rp 0' }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="text-[11px] text-slate-400 dark:text-slate-500 leading-relaxed border-t border-slate-200 dark:border-slate-800 pt-4">
            Notes: This payroll calculation is automatically calculated based on your active roster on board the vessel and is subject to audit. For inquiries, contact HR Department.
          </div>
        </div>

        <div class="flex justify-end gap-3 mt-6">
          <button @click="showPayslipDialog = false" class="px-4 py-2 rounded-lg border border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 font-semibold text-sm hover:bg-slate-50 dark:hover:bg-slate-800">
            Cancel
          </button>
          <button @click="printPayslip" class="px-4 py-2 rounded-lg bg-[var(--color-saipem-tertiary)] text-white font-semibold text-sm hover:bg-[var(--color-saipem-tertiary)]/90">
            Print
          </button>
        </div>
      </div>
    </div>

    <!-- Permit Detail Dialog -->
    <PermitDetailDialog
      v-model:open="showDetailDialog"
      :permit-id="selectedPermitId"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import DataTable from './worker-dashboard/data-table.vue';
import PermitDetailDialog from './PermitDetailDialog.vue';
import { createWorkerColumns } from './worker-dashboard/columns';
import { authState, getAccessToken } from '@/store/auth';
import { toast } from 'vue-sonner';

const props = defineProps({
    myPTWs: {
        type: Array,
        default: () => []
    }
});

const emit = defineEmits(['start-work', 'mark-done', 'edit', 'delete', 'open-submit-modal']);

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1';

const activeTab = ref('permits');
const employeeDetail = ref(null);
const myRosters = ref([]);
const myCertifications = ref([]);
const myPayroll = ref(null);
const vesselActivities = ref([]);
const showPayslipDialog = ref(false);
const showDetailDialog = ref(false);
const selectedPermitId = ref(null);

const isLoading = ref(true);

const userInitial = computed(() => {
    const name = employeeDetail.value?.full_name || authState.username || 'W';
    return name.charAt(0).toUpperCase();
});

const activeRoster = computed(() => {
    const todayStr = new Date().toISOString().split('T')[0];
    return myRosters.value.find(r => r.start <= todayStr && r.end >= todayStr) || myRosters.value[0] || null;
});

const remainingDays = computed(() => {
    if (!activeRoster.value) return 0;
    const today = new Date();
    today.setHours(0,0,0,0);
    const end = new Date(activeRoster.value.end);
    const diffTime = end.getTime() - today.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays > 0 ? diffDays : 0;
});

const activePermitsCount = computed(() => {
    return props.myPTWs.filter(p => p.status === 'APPROVED' || p.status === 'IN_PROGRESS').length;
});

const pendingPermitsCount = computed(() => {
    return props.myPTWs.filter(p => p.status === 'PENDING').length;
});

const filteredActivities = computed(() => {
    if (!activeRoster.value) return [];
    return vesselActivities.value.filter(act => act.asset_name === activeRoster.value.vessel_name);
});

const affectedAssets = computed(() => {
    const assetsMap = new Map();
    props.myPTWs.forEach(ptw => {
        if (ptw.work_order && ptw.work_order.target_asset && ptw.work_order.target_asset !== '-') {
            const assetName = ptw.work_order.target_asset;
            const status = ptw.status_display || ptw.status;
            
            if (!assetsMap.has(assetName)) {
                assetsMap.set(assetName, {
                    name: assetName,
                    permitsCount: 1,
                    latestPermitStatus: status
                });
            } else {
                const current = assetsMap.get(assetName);
                current.permitsCount += 1;
                current.latestPermitStatus = status;
            }
        }
    });
    return Array.from(assetsMap.values());
});

const handleView = (row) => {
    selectedPermitId.value = row.id;
    showDetailDialog.value = true;
};

const columns = createWorkerColumns({
    onStartWork: (id) => emit('start-work', id),
    onMarkDone: (id) => emit('mark-done', id),
    onEdit: (row) => emit('edit', row),
    onDelete: (id) => emit('delete', id),
    onView: handleView,
});

const fetchWorkerData = async () => {
    isLoading.value = true;
    const token = getAccessToken();
    const headers = {
        'Authorization': `Bearer ${token}`
    };
    
    try {
        // 1. Fetch Employee details
        const empRes = await fetch(`${API_BASE_URL}/hr/employees/`, { headers });
        if (empRes.ok) {
            const employees = await empRes.json();
            employeeDetail.value = employees.find(e => e.emp_id === authState.username) || null;
        }

        // 2. Fetch rosters
        const rosterRes = await fetch(`${API_BASE_URL}/hr/rosters/`, { headers });
        if (rosterRes.ok) {
            const rosters = await rosterRes.json();
            myRosters.value = rosters.filter(r => r.employee === authState.username);
        }

        // 3. Fetch certifications
        const certRes = await fetch(`${API_BASE_URL}/hr/certifications/${authState.username}/`, { headers });
        if (certRes.ok) {
            myCertifications.value = await certRes.json();
        }

        // 4. Fetch payroll
        const payrollRes = await fetch(`${API_BASE_URL}/hr/payroll/`, { headers });
        if (payrollRes.ok) {
            const payrolls = await payrollRes.json();
            myPayroll.value = payrolls.find(p => p.emp_id === authState.username) || null;
        }

        // 5. Fetch vessel activities
        const activityRes = await fetch(`${API_BASE_URL}/hr/activities/`, { headers });
        if (activityRes.ok) {
            vesselActivities.value = await activityRes.json();
        }
    } catch (err) {
        console.error("Error fetching worker dashboard data:", err);
        toast.error("Failed to load some dashboard details.");
    } finally {
        isLoading.value = false;
    }
};

const formatDate = (dateStr) => {
    if (!dateStr) return '-';
    try {
        const d = new Date(dateStr);
        return d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' });
    } catch {
        return dateStr;
    }
};

const isExpired = (expiryStr) => {
    if (!expiryStr) return false;
    return new Date(expiryStr) < new Date();
};

const isCurrentRoster = (roster) => {
    const todayStr = new Date().toISOString().split('T')[0];
    return roster.start <= todayStr && roster.end >= todayStr;
};

const formatRupiah = (val) => {
    if (val === undefined || val === null) return null;
    return new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: 'IDR',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(val);
};

const printPayslip = () => {
    const printContent = document.getElementById('print-payslip')?.innerHTML;
    if (!printContent) return;
    
    const originalContent = document.body.innerHTML;
    const printWindow = window.open('', '_blank');
    if (!printWindow) return;
    
    printWindow.document.write(`
        <` + `html>
        <head>
            <title>Payslip Statement - ${authState.username}</title>
            <style>
                body { font-family: sans-serif; padding: 40px; color: #333; }
                .text-right { text-align: right; }
                .flex { display: flex; justify-content: space-between; }
                .pb-4 { padding-bottom: 16px; }
                .border-b { border-bottom: 1px solid #ddd; }
                .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 20px 0; }
                .text-xs { font-size: 12px; }
                .text-sm { font-size: 14px; }
                .text-slate-400 { color: #888; }
                .font-semibold { font-weight: 600; }
                .font-bold { font-weight: bold; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { padding: 12px; border: 1px solid #ddd; text-align: left; }
                th { background-color: #f9f9f9; color: #555; }
                .bg-slate-50 { background-color: #f9f9f9; }
                .text-right-align { text-align: right; }
                .text-center-align { text-align: center; }
            </style>
        </head>
        <` + `body>
            ${printContent}
            <` + `script>
                window.onload = function() {
                    window.print();
                    window.close();
                }
            <` + `/script>
        <` + `/body>
        <` + `/html>
    `);
    printWindow.document.close();
};

onMounted(() => {
    fetchWorkerData();
});
</script>
