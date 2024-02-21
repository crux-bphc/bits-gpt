<script lang="ts">
    import { onMount } from 'svelte';
    import { writable } from 'svelte/store';
  
    interface Message {
      text: string;
    }
  
    const messages = writable<Message[]>([]);
    let messageInput: HTMLInputElement;
  
    function sendMessage() {
      const text = messageInput.value.trim();
      if (text !== '') {
        messages.update(msgs => [...msgs, { text }]);
        messageInput.value = '';
      }
    }
  
    onMount(() => {
      messageInput.focus();
    });
  </script>

  <div class="flex flex-col h-screen justify-between">
    <div class="bg-zinc-800 p-4 h-full overflow-y-auto">
      {#each $messages as message}
        <div class="bg-zinc-600 p-2 my-1 rounded-lg text-white">{message.text}</div>
      {/each}
    </div>
    <div class="bg-zinc-800 p-4">
      <input
        bind:this={messageInput}
        type="text"
        placeholder="Type your message..."
        class="w-11/12 px-4 py-2 bg-zinc-700 rounded-lg text-white focus:outline-none focus:border border-white"
        on:keyup={(e) => e.key === 'Enter' && sendMessage()}
      />
      <button
        class="mt-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:bg-blue-600"
        on:click={sendMessage}
      >

      ➤
      </button>
      <div class="text-gray-100 items-center text-xs mt-3">
        * BitsGPT may display inaccurate info so double-check its responses.
      </div>
    </div>
  </div>
  