<template>
  <DashboardLayout>
    <div class="p-8">
      <!-- Header -->
      <div class="flex justify-between items-start mb-8">
        <div>
          <h2 class="text-3xl font-black text-slate-900 dark:text-white uppercase tracking-tight">User Management</h2>
          <p class="text-sm text-slate-600 dark:text-slate-400 mt-1 font-mono">Manage system accounts, roles, and administrative access</p>
        </div>
        <button @click="openAddModal" class="bg-[var(--color-saipem-tertiary)] hover:bg-orange-600 text-white font-bold px-6 py-3 rounded-lg transition shadow-lg flex items-center gap-2 font-mono text-xs uppercase">
          <Plus class="w-4 h-4" />
          Add User
        </button>
      </div>

      <!-- Users Table -->
      <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-sm overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-slate-50 dark:bg-slate-950 border-b border-slate-200 dark:border-slate-800 font-mono text-[10px]">
              <tr>
                <th class="px-6 py-4 text-left font-bold text-slate-400 uppercase tracking-wider">Username</th>
                <th class="px-6 py-4 text-left font-bold text-slate-400 uppercase tracking-wider">Full Name</th>
                <th class="px-6 py-4 text-left font-bold text-slate-400 uppercase tracking-wider">Email Address</th>
                <th class="px-6 py-4 text-left font-bold text-slate-400 uppercase tracking-wider">System Role</th>
                <th class="px-6 py-4 text-left font-bold text-slate-400 uppercase tracking-wider">Job Title</th>
                <th class="px-6 py-4 text-center font-bold text-slate-400 uppercase tracking-wider">Action</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-slate-800/60 font-mono text-xs">
              <tr v-if="isLoading" class="hover:bg-slate-50/50 dark:hover:bg-slate-900/50">
                <td colspan="6" class="px-6 py-12 text-center">
                  <Loader class="w-8 h-8 animate-spin text-[var(--color-saipem-tertiary)] mx-auto" />
                  <p class="text-slate-500 dark:text-slate-400 mt-3 font-semibold">Loading system accounts...</p>
                </td>
              </tr>
              <tr v-else-if="users.length === 0" class="hover:bg-slate-50/50 dark:hover:bg-slate-900/50">
                <td colspan="6" class="px-6 py-12 text-center text-slate-500 dark:text-slate-400 font-semibold">
                  No system users found.
                </td>
              </tr>
              <tr v-for="user in users" :key="user.id" class="hover:bg-slate-50/30 dark:hover:bg-slate-950/20 transition-colors">
                <td class="px-6 py-4 font-bold text-[var(--color-saipem-tertiary)]">{{ user.username }}</td>
                <td class="px-6 py-4 text-slate-900 dark:text-slate-200 font-sans font-semibold">
                  {{ user.first_name || '-' }} {{ user.last_name || '' }}
                </td>
                <td class="px-6 py-4 text-slate-500 dark:text-slate-400">{{ user.email || '-' }}</td>
                <td class="px-6 py-4">
                  <span :class="['px-2.5 py-1 rounded text-[10px] font-black uppercase tracking-wider', getRoleColor(user.role_name)]">
                    {{ user.role_name }}
                  </span>
                </td>
                <td class="px-6 py-4 text-slate-600 dark:text-slate-350">{{ user.job_role_name || '-' }}</td>
                <td class="px-6 py-4 text-center">
                  <div class="flex items-center justify-center gap-2">
                    <button @click="openEditModal(user)" class="text-blue-500 hover:text-blue-700 p-1.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg transition-colors" title="Edit User">
                      <Edit class="w-4 h-4" />
                    </button>
                    <button @click="deleteUser(user)" class="text-red-500 hover:text-red-700 p-1.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg transition-colors" title="Delete User">
                      <Trash2 class="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Add/Edit User Modal -->
      <div v-if="showModal" class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50 animate-in fade-in duration-200">
        <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-xl max-w-lg w-full p-6 max-h-[90vh] overflow-y-auto font-mono text-xs">
          <div class="flex justify-between items-center pb-4 border-b border-slate-100 dark:border-slate-800">
            <h3 class="text-lg font-heading font-black text-slate-900 dark:text-white uppercase tracking-tight">
              {{ isEditMode ? 'Edit User' : 'Register User' }}
            </h3>
            <button @click="closeModal" class="text-slate-400 hover:text-slate-600 transition-colors">
              <X class="w-5 h-5" />
            </button>
          </div>
          
          <p class="text-xs text-slate-500 dark:text-slate-400 my-4">
            {{ isEditMode ? 'Modify credential attributes and permissions' : 'Set up credentials and security group mapping' }}
          </p>

          <form @submit.prevent="submitForm" class="space-y-4">
            <div>
              <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Username *</label>
              <input
                v-model="formData.username"
                type="text"
                placeholder="e.g. jdoe123"
                class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none focus:border-[var(--color-saipem-tertiary)] disabled:opacity-50 disabled:cursor-not-allowed"
                :disabled="isEditMode"
                required
              />
            </div>

            <div>
              <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">
                Password <span v-if="!isEditMode">*</span>
              </label>
              <input
                v-model="formData.password"
                type="password"
                :placeholder="isEditMode ? 'Leave blank to keep current password' : 'Enter login password'"
                class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none focus:border-[var(--color-saipem-tertiary)]"
                :required="!isEditMode"
              />
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">First Name</label>
                <input
                  v-model="formData.first_name"
                  type="text"
                  placeholder="John"
                  class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none"
                />
              </div>
              <div>
                <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Last Name</label>
                <input
                  v-model="formData.last_name"
                  type="text"
                  placeholder="Doe"
                  class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none"
                />
              </div>
            </div>

            <div>
              <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Email *</label>
              <input
                v-model="formData.email"
                type="email"
                placeholder="john.doe@saipem.com"
                class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none focus:border-[var(--color-saipem-tertiary)]"
                required
              />
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">System Role *</label>
                <select
                  v-model="formData.role"
                  class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none"
                  required
                >
                  <option value="Admin">Admin</option>
                  <option value="HR Staff">HR Staff</option>
                  <option value="Chief Engineer">Chief Engineer</option>
                  <option value="Safety Officer">Safety Officer</option>
                  <option value="Worker">Worker</option>
                </select>
              </div>
              <div>
                <label class="text-slate-400 font-bold uppercase tracking-wider block mb-1">Job Title</label>
                <input
                  v-model="formData.job_role"
                  type="text"
                  placeholder="e.g. Safety Inspector"
                  class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-slate-900 dark:text-slate-100 focus:outline-none"
                />
              </div>
            </div>

            <div class="flex justify-end gap-3 pt-4 border-t border-slate-100 dark:border-slate-800 mt-6">
              <button type="button" @click="closeModal" class="px-4 py-2 border border-slate-200 dark:border-slate-800 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg font-bold transition-colors">
                Cancel
              </button>
              <button type="submit" class="px-4 py-2 bg-[var(--color-saipem-tertiary)] hover:bg-orange-600 text-white rounded-lg font-bold transition-colors">
                {{ isEditMode ? 'Save Changes' : 'Register User' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import DashboardLayout from '@/layouts/DashboardLayout.vue'
import { Plus, Trash2, Edit, Loader, X } from '@lucide/vue'
import { getAccessToken } from '@/store/auth'
import { toast } from 'vue-sonner'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8989/api/v1'

const isLoading = ref(false)
const users = ref([])

const showModal = ref(false)
const isEditMode = ref(false)
const editingUserId = ref(null)

const formData = ref({
  username: '',
  password: '',
  first_name: '',
  last_name: '',
  email: '',
  role: 'Worker',
  job_role: ''
})

const getRoleColor = (role) => {
  switch (role) {
    case 'Admin':
      return 'bg-purple-100 dark:bg-purple-900/30 text-purple-800 dark:text-purple-400 border border-purple-200/50'
    case 'HR Staff':
      return 'bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-400 border border-blue-200/50'
    case 'Chief Engineer':
      return 'bg-amber-100 dark:bg-amber-900/30 text-amber-800 dark:text-amber-400 border border-amber-200/50'
    case 'Safety Officer':
      return 'bg-orange-100 dark:bg-orange-900/30 text-[var(--color-saipem-tertiary)] dark:text-orange-400 border border-orange-200/50'
    case 'Worker':
      return 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200/50'
    default:
      return 'bg-slate-100 dark:bg-slate-800 text-slate-600'
  }
}

const fetchUsers = async () => {
  isLoading.value = true
  try {
    const response = await fetch(`${API_BASE_URL}/auth/users/`, {
      headers: {
        'Authorization': `Bearer ${getAccessToken()}`
      }
    })
    if (response.ok) {
      users.value = await response.json()
    } else {
      toast.error('Failed', { description: 'Failed to fetch user directory.' })
    }
  } catch (error) {
    console.error('Error fetching users:', error)
    toast.error('Error', { description: 'Server connection failed.' })
  } finally {
    isLoading.value = false
  }
}

const openAddModal = () => {
  isEditMode.value = false
  editingUserId.value = null
  formData.value = {
    username: '',
    password: '',
    first_name: '',
    last_name: '',
    email: '',
    role: 'Worker',
    job_role: ''
  }
  showModal.value = true
}

const openEditModal = (user) => {
  isEditMode.value = true
  editingUserId.value = user.id
  formData.value = {
    username: user.username,
    password: '',
    first_name: user.first_name || '',
    last_name: user.last_name || '',
    email: user.email || '',
    role: user.role_name || 'Worker',
    job_role: user.job_role_name || ''
  }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const submitForm = async () => {
  try {
    const payload = { ...formData.value }
    // If edit mode and password is blank, don't send it
    if (isEditMode.value && !payload.password) {
      delete payload.password
    }

    const url = isEditMode.value 
      ? `${API_BASE_URL}/auth/users/${editingUserId.value}/`
      : `${API_BASE_URL}/auth/users/`

    const response = await fetch(url, {
      method: isEditMode.value ? 'PUT' : 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getAccessToken()}`
      },
      body: JSON.stringify(payload)
    })

    if (response.ok) {
      toast.success('Success', { description: `User account ${isEditMode.value ? 'updated' : 'registered'} successfully.` })
      showModal.value = false
      fetchUsers()
    } else {
      const errorData = await response.json()
      const msg = Object.values(errorData).flat()[0] || 'Operation failed.'
      toast.error('Failed', { description: msg })
    }
  } catch (error) {
    console.error('Error submitting form:', error)
    toast.error('Error', { description: 'Connection failed.' })
  }
}

const deleteUser = async (user) => {
  if (!confirm(`Are you sure you want to delete user account "${user.username}"?`)) return
  try {
    const response = await fetch(`${API_BASE_URL}/auth/users/${user.id}/`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${getAccessToken()}`
      }
    })

    if (response.ok) {
      toast.success('Deleted', { description: 'User account deleted successfully.' })
      fetchUsers()
    } else {
      toast.error('Failed', { description: 'Failed to delete user account.' })
    }
  } catch (error) {
    console.error('Error deleting user:', error)
    toast.error('Error', { description: 'Connection failed.' })
  }
}

onMounted(() => {
  fetchUsers()
})
</script>
