<script lang="ts" setup>
import { ref, onMounted, computed } from "vue"
import axios from 'axios'
import type { VxeGridProps, VxeTableEvents } from 'vxe-table'

interface FilterField {
    field: string
    lookup?: string
    label: string
    type: 'text' | 'select' | 'number' | 'range' | 'daterange'
    placeholder?: string
    options?: Array<{ value: any; label: string; }>
    multiple?: boolean
}
interface Schema {
    filters: FilterField[]
    columns: Array<{ field: string, title: string, width: string, sortable?: boolean }>
}

const schema = ref<Schema | null>(null)
const tableData = ref<any[]>([])
const loading = ref<boolean>(false)
const filtersForm = ref<Record<string, any>>({})
const queryParams = ref<Record<string, any>>({})

const fetchSchemaAndData = async () => {
    loading.value = true
    try {
        const schemaRes = await axios.get('api/products/filters/')
        console.log("schemaRes.data:", schemaRes.data)
        schema.value = schemaRes.data

        schema.value?.filters.forEach((f: FilterField) => {
            if (f.type === 'range') {
                filtersForm.value[`${f.field}__gte`] = ''
                filtersForm.value[`${f.field}__lte`] = ''
            } else {
                const key = getFilterKey(f)
                filtersForm.value[key] = ''
            }
        })
        await fetchTableData()
    } catch (err) {
        console.error(err)
    } finally {
        loading.value = false
    }


}
const fetchTableData = async () => {
    loading.value = true
    try {
        const res = await axios.get('api/products/', {
            params: queryParams.value
        })
        tableData.value = res.data.results || res.data
    } catch (err) {
        console.error(err)
    } finally {
        loading.value = false
    }
}

const handleFilterApply = async () => {
    // 过滤掉空字符串，只将有值的参数同步到 queryParams
    const activeParams: Record<string, any> = {}
    Object.keys(filtersForm.value).forEach(key => {
        if (filtersForm.value[key] !== '' && filtersForm.value[key] !== null) {
            activeParams[key] = filtersForm.value[key]
        }
    })
    queryParams.value = activeParams
    fetchTableData()
}

const handleReset = async () => {
    Object.keys(filtersForm.value).forEach((key) => {
        filtersForm.value[key] = ''
    })
    queryParams.value = {}
    await fetchTableData()
}
const getFilterKey = (f: FilterField) => {
    return (f.lookup && f.lookup !== 'exact') ? `${f.field}__${f.lookup}` : f.field
}

onMounted(fetchSchemaAndData)
</script>

<template>
    <div v-if="schema" class="bg-white p-6 rounded-2xl shadow mb-6">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="f in schema?.filters" :key="f.field">
                <label class="block text-sm font-medium text-gray-700 mb-2">{{ f.label }}</label>
                <template v-if="f.type === 'text' || f.type === 'number'">
                    <input v-model="filtersForm[getFilterKey(f)]" :type="f.type" :placeholder="f.placeholder"
                        class="border border-gray-300 px-3 py-2 rounded w-full" />
                </template>

                <template v-else-if="f.type === 'select' && f.options">
                    <select v-model="filtersForm[getFilterKey(f)]"
                        class="border border-gray-300 px-3 py-2 rounded w-full">
                        <option value="">全部</option>
                        <option v-for="opt in f.options" :key="opt.value" :value="opt.value">
                            {{ opt.label }}
                        </option>
                    </select>
                </template>

                <template v-else-if="f.type === 'range'">
                    <div class="flex gap-2">
                        <input v-model="filtersForm[`${f.field}__gte`]" type="number"
                            class="border border-gray-300 px-3 py-2 rounded flex-1" />
                        <span class="self-center">至</span>
                        <input v-model="filtersForm[`${f.field}__lte`]" type="number"
                            class="border border-gray-300 px-3 py-2 rounded flex-1" />
                    </div>
                </template>

                <template v-else>
                    <span>未知类型</span>
                </template>
            </div>
        </div>
        <div class="mt-8 flex gap-4">
            <button @click="handleFilterApply" class="px-6 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700">
                筛选
            </button>
            <button @click="handleReset" class="px-6 py-2 border border-gray-300 rounded-xl hover:bg-gray-50">
                重置
            </button>
        </div>
    </div>
    <div>
        <vxe-grid v-if="schema" v-model:loading="loading" :data="tableData" :columns="schema.columns" height="500px"
            :border="true" :resizable="true" :sortable="true" show-overflow />
    </div>
</template>
