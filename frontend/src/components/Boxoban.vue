<template>
  <div ref="boxoban">
        <div class=" flex justify-between text-gray-800 text-lg font-light mt-4">
            <div class="text-right">Solved: 
              <span v-if="solved" class="relative inline-block px-3 py-1 font-semibold text-green-900 leading-tight">
                  <span aria-hidden="true" class="absolute inset-0 bg-green-200 opacity-50 rounded-full">
                  </span>
                  <span class="relative m-3">
                      ✓
                  </span>
              </span>
              <span v-if="!solved" class="relative inline-block px-3 py-1 font-semibold text-red-900 leading-tight">
                  <span aria-hidden="true" class="absolute inset-0 bg-red-200 opacity-50 rounded-full">
                  </span>
                  <span class="relative m-3">
                      ☓
                  </span>
              </span>
            </div>
            <div class="text-left">Steps: <span  class="w-4 inline-block">{{steps}}</span></div>
        </div>
    <screen :room="room" ref="screen" class="mx-auto mt-12"/>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { onKeyStroke, useElementVisibility, useWindowSize, debouncedWatch } from '@vueuse/core'
import confetti from 'canvas-confetti'
import axios from 'axios'

import Environment from '../environment'
import Screen from './Screen.vue'

const props = defineProps({
  room: Array,
  topology: Array,
  control: {
    type: Boolean,
    default: true,
  },
})

const boxoban = ref(null)
const screen = ref(null)
const steps = ref(0)
const addedSteps = ref(0)
const solved = ref(false)
const room = reactive(JSON.parse(JSON.stringify(props.room)))
let environment = new Environment(room, props.topology)


const { width: windowWidth, height: windowHeight } = useWindowSize()
const boxobanIsVisible = useElementVisibility(boxoban)

if (props.control == true) {
  onKeyStroke('ArrowUp', (e) => {
    e.preventDefault()
    addedSteps.value += 1
    step(0)
  })
  onKeyStroke('ArrowDown', (e) => {
    e.preventDefault()
    addedSteps.value += 1
    step(1)
  })
  onKeyStroke('ArrowLeft', (e) => {
    e.preventDefault()
    addedSteps.value += 1
    step(2)
  })
  onKeyStroke('ArrowRight', (e) => {
    e.preventDefault()
    addedSteps.value += 1
    step(3)
  })

  debouncedWatch(
    addedSteps,
    updateSteps,
    { debounce: 2000 }
  )
}

async function step(action) {
  if (!boxobanIsVisible.value) {
    return
  }

  steps.value += 1
  let result = environment.step(action)

  if (result.info.finished == false){
    solved.value = false
  }

  if (result.done == true && result.info.finished == true) {
    solved.value = true

    for (let i = 0; i <3; i++) {
      celebrate()
      await new Promise((r) => setTimeout(r, 350))
    }
}

function celebrate(){
    const { left, top, width, height } = screen.value.$el.getBoundingClientRect()

    confetti({
      particleCount: 250,
      spread: 80,
      ticks: 100,
      gravity: 1.5,
      origin: {
        x: (left + width / 2) / windowWidth.value,
        y: (top + height / 12 * 7) / windowHeight.value,
      },
    })
  }
}

async function stepTrajectory(actions){
  for (let action of actions) {
    await new Promise((r) => setTimeout(r, 450))
    step(action)
  }
}

function reset(){
  for (let i=0; i<=9; i++) {
    for (let j=0; j<=9; j++){
      room[i][j] = props.room[i][j]
    }
  }
  environment = new Environment(room, props.topology)
  steps.value = 0
  solved.value = false
}

async function updateSteps(){
  let number = addedSteps.value
    
  if (number <= 0) {
    return
  }

  try {
      addedSteps.value = 0

      const formData = new FormData();
      formData.append("steps", number);

      await axios.patch("/api/steps",  formData);
  } catch (error) {
      console.error(error)
  } 
}

defineExpose({
  stepTrajectory,
  reset,
})
</script>


