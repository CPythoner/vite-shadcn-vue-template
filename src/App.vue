<script setup lang="ts">
import HelloWorld from './components/HelloWorld.vue'
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
</script>

<template>
  <div class="min-h-screen bg-background text-foreground flex flex-col items-center justify-center p-4">
    <Card class="w-full max-w-md">
      <CardHeader>
        <CardTitle class="text-2xl font-bold text-center">Vite + Vue + shadcn</CardTitle>
      </CardHeader>
      <CardContent>
        <div class="flex justify-center space-x-4 mb-6">
          <a href="https://vitejs.dev" target="_blank" class="hover:opacity-80 transition-opacity">
            <img src="/vite.svg" class="h-12" alt="Vite logo" />
          </a>
          <a href="https://vuejs.org/" target="_blank" class="hover:opacity-80 transition-opacity">
            <img src="./assets/vue.svg" class="h-12" alt="Vue logo" />
          </a>
        </div>
        <HelloWorld msg="Vite + Vue" />
        <div class="mt-6 flex justify-center">
          <Button>Click me</Button>
        </div>
      </CardContent>
    </Card>
  </div>
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
