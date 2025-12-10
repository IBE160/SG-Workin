"use client"

import { ChatWindow, Message } from '@/components/modules/chat/ChatWindow'
import { ChatInput } from '@/components/modules/chat/ChatInput'
import { useState } from 'react'

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)

  const handleSendMessage = async (text: string) => {
    // Add user message immediately
    const userMsg: Message = { role: 'user', content: text }
    setMessages(prev => [...prev, userMsg])
    setIsLoading(true)

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000/api'
      const response = await fetch(`${apiUrl}/messages`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: text }),
      })

      if (!response.ok) {
        throw new Error('Network response was not ok')
      }

      const data = await response.json()
      // data.data.response contains the bot's text
      const botMsg: Message = { role: 'assistant', content: data.data.response }
      setMessages(prev => [...prev, botMsg])
    } catch (error) {
      console.error('Error sending message:', error)
      const errorMsg: Message = { role: 'assistant', content: 'Sorry, something went wrong.' }
      setMessages(prev => [...prev, errorMsg])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm lg:flex">
        <h1 className="text-4xl font-bold text-center w-full mb-8">Chat</h1>
      </div>

      <ChatWindow messages={messages} />

      <div className="fixed bottom-0 left-0 w-full p-4 bg-background border-t">
        <div className="max-w-5xl mx-auto">
          <ChatInput onSend={handleSendMessage} isLoading={isLoading} />
        </div>
      </div>
    </main>
  )
}
