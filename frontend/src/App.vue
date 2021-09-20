<template>
<div class="bg-indigo-900 relative overflow-hidden h-screen">
    <img :src="hero" class="absolute h-full w-full object-cover"/>
    <div class="inset-0 bg-black opacity-25 absolute">
    </div>
    <div class="container mx-auto px-6 md:px-12 relative z-10 flex items-center py-24 xl:py-40">
        <div class="w-full flex flex-col items-center relative z-10">
            <h1 class="font-sans font-semibold text-5xl text-center text-white leading-tight mt-4">
               Solving Sokoban puzzle using <br/>
               multiple reinforcement learning methods
            </h1>
            <a @click="scrollIntoControlBar" class="block cursor-pointer bg-gray-800 hover:bg-gray-900 py-3 px-4 text-lg text-white font-bold uppercase mt-14">
                Try Now
            </a>
        </div>
    </div>
    <kinesis-container event="scroll" class="absolute box bottom-20"> 
      <kinesis-element 
            tag="img"
            :src="heroBox"
            :strength="400"
            type="translate"
            axis="x"
            >
        </kinesis-element>
    </kinesis-container>

</div>

<div class="flex justify-around mt-20 mb-12"  ref="stepCounter">
<div class="text-2xl text-gray-900 font-normal">
    Total number of steps performed by players to defeat the AI
    <div class="text-center mt-7 font-semibold text-3xl">{{animatedTotalSteps}}</div>
</div>
</div>


<div class="flex justify-around mt-20 mb-10"  ref="controlBar">
<p class="text-2xl text-gray-900 font-medium">
    Level id: {{levelId}}
</p>

<div class="flex justify-between">
<button @click="nextLevel" class="mr-8 px-6 py-2  transition ease-in duration-200 uppercase rounded-full hover:bg-gray-800 hover:text-white border-2 border-gray-900 focus:outline-none">
    Next level
</button>
<button @click="randomLevel" class="mr-8 px-6 py-2  transition ease-in duration-200 uppercase rounded-full hover:bg-gray-800 hover:text-white border-2 border-gray-900 focus:outline-none">
    Random level 
</button>
<button @click="findLevel" class="mr-8 px-6 py-2  transition ease-in duration-200 uppercase rounded-full hover:bg-gray-800 hover:text-white border-2 border-gray-900 focus:outline-none">
    Fetch a level by id
</button>
<button @click="reset" class="mr-8 px-6 py-2  transition ease-in duration-200 uppercase rounded-full hover:bg-gray-800 hover:text-white border-2 border-gray-900 focus:outline-none">
    Reset level
</button>
</div>

</div>

<div class="flex items-stretch">
 <div class="w-1/2 flex justify-center items-top">
    <div class="w-full p-4">
        <div class="card flex flex-col justify-start h-full p-10 bg-white rounded-lg shadow-md hover:shadow-2xl transition-shadow duration-500">
            <div class="prod-title">
                <p class="text-2xl uppercase text-gray-900 font-bold">
                    Human
                </p>
                <p class="text-sm text-gray-400 mt-2">
                   The goal is to push all the yellow boxes on top of the red targets. <br/> 
                   Use the arrow keys to move the agent. <br/>
                   Try to pass the level with as few steps as possible to <span class="uppercase text-gray-800 text-base font-semibold">beat the AI!</span>
                </p>
            </div>
            <div>
              <boxoban :room="room" :topology="topology" :control="true" ref="human" class="my-10"/>
              </div>
        </div>
    </div>
</div>

<div class="w-1/2 flex justify-center items-top">
    <div class="w-full p-4">
        <div class="card flex flex-col justify-start p-10 bg-white rounded-lg shadow-md hover:shadow-2xl transition-shadow duration-500">
            <div class="prod-title">
                <p class="text-2xl uppercase text-gray-900 font-bold">
                    AI
                </p>
                <p class="text-sm text-gray-400 mt-2">
                   AI is the best performing GAIL ResNet model among the reinforcement learning algorithms experimented in the dissertation.<br/> 
                   Click the solve button to let AI solve the level.
                </p>
            </div>
            <div>
              <boxoban :room="room" :topology="topology" :control="false" ref="ai" class="my-10"/>
                <button @click="solve" class="m-auto block px-12 py-2  transition ease-in duration-200 uppercase rounded-full hover:bg-gray-800 hover:text-white border-2 border-gray-900 focus:outline-none">
                    <svg v-show="solveLoading" class="animate-spin -ml-1 mr-2 h-5 w-5 inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Solve
                </button>
                <div :class="{ 'opacity-100': solvedVisibility, 'opacity-0': !solvedVisibility}" class="text-base text-gray-700 mt-6 text-center transition-all duration-1000 ease-in-out">
                    <div v-if="solved">AI successfully solves this level, watch out for the Skynet!</div>
                    <div v-if="!solved">AI  can't solve this level, it can't rule the world yet!</div>
                </div>
              </div>
        </div>
    </div>
</div>
</div>


<footer class="bg-white mt-28 w-full py-4 border-gray-200">
    <div class="max-w-screen-xl mx-auto px-4">
        <!-- <a href="https://github.com/binaryoung/COMP4026-MSc-Projects" target="_blank" class="text-center text-gray-400 hover:text-gray-800  transition-colors duration-150 pt-8 sm:pt-2 font-light flex items-center justify-center">
                Code for the dissertation
        </a> -->
        <span class="text-center text-gray-400  pt-10 sm:pt-2 font-light flex items-center justify-center">
                Copyright © 2021&nbsp;<a href="https://github.com/binaryoung" target="_blank" class="text-center text-gray-400 hover:text-gray-800  transition-colors duration-150 font-light">Young</a>
        </span>
    </div>
</footer>
</template>

<style scoped>
.box {
    left: 60%;
  	filter: brightness(80%);
}
footer{
    	border-top-width: 1px;
}
</style>

<script setup>
import {ref, computed, watch, onMounted } from 'vue'
import { KinesisContainer, KinesisElement} from 'vue-kinesis'
import { useIntervalFn, useElementVisibility, useTransition} from '@vueuse/core'
import { useNProgress } from '@vueuse/integrations/useNProgress'
import axios from 'axios'

import Boxoban from './components/Boxoban.vue'
import hero from './assets/sokoban.png'
import heroBox from './assets/hero-box.png'
import wall from './assets/wall.png'
import floor from './assets/floor.png'
import target from './assets/target.png'
import box from './assets/box.png'
import boxOnTarget from './assets/box_on_target.png'
import player from './assets/player.png'
import playerOnTarget from './assets/player_on_target.png'

const totalSteps = ref(0)
const stepCounter = ref(null)
const controlBar = ref(null)
const human = ref(null)
const ai = ref(null)
const levelId = ref(0)
const solved = ref(false)
const solvedVisibility = ref(false)
const solveLoading = ref(false)

const { isLoading } = useNProgress()
const stepCounterIsVisible = useElementVisibility(stepCounter)

let room = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,1,1,1,1,2,1,0],
    [0,0,1,2,1,1,1,3,2,0],
    [0,0,1,1,1,1,2,3,1,0],
    [0,0,0,0,0,1,1,1,1,0],
    [0,0,0,0,1,1,1,0,0,0],
    [0,0,0,0,0,1,3,0,0,0],
    [0,0,0,0,0,3,1,0,0,0],
    [0,0,0,0,0,5,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0]
]

let topology = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,1,1,1,1,2,1,0],
    [0,0,1,2,1,1,1,1,2,0],
    [0,0,1,1,1,1,2,1,1,0],
    [0,0,0,0,0,1,1,1,1,0],
    [0,0,0,0,1,1,1,0,0,0],
    [0,0,0,0,0,1,1,0,0,0],
    [0,0,0,0,0,1,1,0,0,0],
    [0,0,0,0,0,1,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0]
]

onMounted(() => {
    for (let image of [wall, floor, target, box, boxOnTarget, player, playerOnTarget]) {
        let img=new Image();
        img.src=image;
    }
})

async function fetchSteps(){
    try {
        const {data: {steps}} = await axios.get("/api/steps");

        totalSteps.value = steps
    } catch (error) {
        console.error(error)
    } 
}

const transitionTotalSteps = useTransition(totalSteps, {
  duration: 1000,
})

const animatedTotalSteps = computed(() => {
  return transitionTotalSteps.value.toFixed(0)
})

useIntervalFn(() => {
    if (stepCounterIsVisible.value) {
        fetchSteps()
    }
}, 3000)

watch(stepCounterIsVisible, (newValue, oldValue) => {
  if (newValue == true) {
    fetchSteps()
  }
})

fetchSteps()

function scrollIntoControlBar(){
    controlBar.value.scrollIntoView({behavior: 'smooth'})
}

function nextLevel(){
    let id = (levelId.value + 1) % 1000

    fetchLevel(id)
}

function randomLevel(){
    let id = Math.floor(Math.random() * 999)

    fetchLevel(id)
}

function findLevel(){
    let id = prompt("Enter a level id between 0 and 999")
    id =  parseInt(id)

    if (id === null || isNaN(id)) {
        return
    }

    if (id < 0 || id > 999){
        alert("Level id must be between 0 and 999")
        return
    }

    fetchLevel(id)
}

async function fetchLevel(id){
    try {
        isLoading.value = true

        const {data} = await axios.get(`/api/levels/${id}`);

        levelId.value = data.id
        for (let i=0; i<=9; i++) {
            for (let j=0; j<=9; j++){
                room[i][j] = data.room[i][j]
                topology[i][j]  = data.topology[i][j]
            }
        }
        reset()
    } catch (error) {
        console.error(error)
        alert("An error occurred, please try again")
    } finally {
        isLoading.value = false
    }
}

function reset() {
    human.value.reset()
    ai.value.reset()
}

async function solve() {
    try {
        isLoading.value = true
        solveLoading.value = true

        const {data} = await axios.get(`/api/levels/${levelId.value}/solve`);

        solved.value = data.solved

        solvedVisibility.value = true
        setTimeout(() => solvedVisibility.value = false, 5000);

        if (data.solved) {
            ai.value.stepTrajectory(data.trajectory)
        }
    } catch (error) {
        console.error(error)
        if (error.response.status == 429) {
            alert("Too many requests, please try again later")
        } else {
            alert("An error occurred, please try again")
        }
    } finally {
        isLoading.value = false
        solveLoading.value = false
    }
}


</script>