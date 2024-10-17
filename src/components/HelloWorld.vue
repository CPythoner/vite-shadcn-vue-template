<script setup lang="ts">
import { ref } from 'vue'
import { Button } from "@/components/ui/button"

defineProps<{ msg: string }>()

const count = ref(0)
</script>

<template>
  <div class="text-center">
    <h1 class="text-3xl font-bold mb-4">{{ msg }}</h1>

    <div class="mb-4">
      <Button @click="count++">count is {{ count }}</Button>
    </div>

    <p class="mb-2 text-sm text-muted-foreground">
      Edit <code class="font-mono bg-muted px-1 py-0.5 rounded">components/HelloWorld.vue</code> to test HMR
    </p>

    <p class="mb-2 text-sm">
      Check out
      <a href="https://vuejs.org/guide/quick-start.html#local" target="_blank" class="text-primary hover:underline">create-vue</a>, the official Vue + Vite starter
    </p>
    <p class="mb-2 text-sm">
      Learn more about IDE Support for Vue in the
      <a href="https://vuejs.org/guide/scaling-up/tooling.html#ide-support" target="_blank" class="text-primary hover:underline">Vue Docs Scaling up Guide</a>.
    </p>
    <p class="text-sm text-muted-foreground">Click on the Vite and Vue logos to learn more</p>
  </div>
</template>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
