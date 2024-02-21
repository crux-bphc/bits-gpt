<script lang="ts">
    import { onMount } from 'svelte';
    import { writable } from 'svelte/store';
  
    interface Message {
      author: string;
      text: string;
    }
  
    const messages = writable<Message[]>([]);
    messages.update(msgs => [...msgs, {author: "BitsGPT", text: "Hello! I'm BitsGPT, the campus buddy chatbot for making your student life easier. Feel free to ask me anything!"}]);
    
    let messageInput: HTMLInputElement;
  
    function sendMessage() {
      const text = messageInput.value.trim();
      const author = 'You';
      if (text !== '') {
        messages.update(msgs => [...msgs, {author, text}]);
        messageInput.value = '';

        fetch('http://172.16.142.163:8000/talk/invoke', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({input: text})
        }).then(response => response.json())
          .then(data => {
            messages.update(msgs => [...msgs, {author: "BitsGPT", text: data.output}]);
          });
      };
    }
  
    onMount(() => {
      messageInput.focus();
    });
  </script>

  <div>
    

  <div class="bg-zinc-900 flex flex-col h-screen justify-between">
    
    <div class=" p-4 text-white text-5xl font-semibold flex flex-row">
        <img src="crux.png" alt="Crux Logo" class="w-16 h-16" />
        <span class="mt-1 ml-3">BitsGPT</span> 
        <span class="ml-2  text-gray-400 text-3xl mt-4">v1.0.0</span>
    </div>
    <div class="p-4 h-full overflow-y-auto text-lg">
      {#each $messages as message}
        <div class="bg-zinc-600 p-2 my-2 w-1/2 mx-auto rounded-lg text-white whitespace-pre-wrap">
          <span class="font-bold">{message.author}:</span>
          {message.text}
        </div>
      {/each}
    </div>
    <div class="w-1/2 mx-auto relative flex items-center ">
      <input
        bind:this={messageInput}
        type="text"
        placeholder="Type your message..."
        class="px-4 py-2 w-full bg-zinc-700 rounded-lg text-lg text-white focus:outline-none focus:border border-white"
        on:keyup={(e) => e.key === 'Enter' && sendMessage()}
      />
      <button
        class="ml-2 px-4 py-2 bg-blue-500 text-white rounded-lg text-lg hover:bg-blue-600 focus:outline-none focus:bg-blue-600"
        on:click={sendMessage}
      >

      ➤
      </button>
    </div>
    <div class=" text-gray-200 items-center text-sm pl-4 pb-4 w-1/2 mt-2 mx-auto">
      * BitsGPT may display inaccurate info so double-check its responses.
    </div>
  </div>
</div>