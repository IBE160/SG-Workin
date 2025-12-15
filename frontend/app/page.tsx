
"use client"

import { ChatWindow, Message } from '@/components/modules/chat/ChatWindow'
import { ChatInput } from '@/components/modules/chat/ChatInput'
import { useState } from 'react'

import { Trash2, MessageSquarePlus } from "lucide-react"
import { EndChatModal } from '@/components/modules/chat/EndChatModal'
import { LogOut } from "lucide-react"

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [showEndChat, setShowEndChat] = useState(false)

  const handleSendMessage = async (text: string) => {
    // Add user message immediately
    const userMsg: Message = { role: 'user', content: text }
    setMessages(prev => [...prev, userMsg])
    setIsLoading(true)

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000/api'
      // Convert history to format expected by backend (excluding current message)
      const history = messages.map(m => ({
        role: m.role,
        content: m.content
      }))

      const response = await fetch(`${apiUrl}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: text,
          history: history
        }),
      })

      if (!response.ok) {
        throw new Error('Network response was not ok')
      }

      const data = await response.json()
      // data.data.response contains the bot's text
      const botMsg: Message = {
        role: 'assistant',
        content: data.data.response,
        type: data.data.type,
        escalationLink: data.data.escalation_link,
        sources: data.data.sources // Extract sources from API
      }
      setMessages(prev => [...prev, botMsg])
    } catch (error) {
      console.error('Error sending message:', error)
      const errorMsg: Message = { role: 'assistant', content: 'Sorry, something went wrong. Please try again later.' }
      setMessages(prev => [...prev, errorMsg])
    } finally {
      setIsLoading(false)
    }
  }

  const handleClearChat = () => {
    setMessages([])
  }

  const handleEndChatSubmit = async (score: number, comment: string, email: string) => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000/api'

      // Prepare chat history for transcript
      const history = messages.map(m => ({
        role: m.role,
        content: m.content
      }))

      await fetch(`${apiUrl}/transcript`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: email || null,
          chat_history: history,
          rating: score,
          comment: comment
        })
      })

      // Clear chat after successful submission
      setMessages([])

    } catch (e) {
      console.error("End Chat failed", e)
    }
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24 relative">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm lg:flex">
        <h1 className="text-4xl font-bold text-center w-full mb-8">Chat</h1>
      </div>

      <ChatWindow messages={messages} />

      {/* End Chat Modal Overlay */}
      {showEndChat && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-background rounded-lg shadow-xl">
            <EndChatModal
              onSubmit={handleEndChatSubmit}
              onClose={() => setShowEndChat(false)}
            />
          </div>
        </div>
      )}

      <div className="fixed bottom-0 left-0 w-full p-4 bg-background border-t z-40">
        <div className="max-w-5xl mx-auto flex items-center gap-4">
          <button
            onClick={handleClearChat}
            className="p-2 text-muted-foreground/50 hover:text-destructive transition-colors rounded-full hover:bg-muted"
            title="Clear Chat"
            aria-label="Clear Chat"
          >
            <Trash2 className="w-5 h-5" />
          </button>

          <button
            onClick={() => setShowEndChat(true)}
            className="p-2 text-muted-foreground/50 hover:text-destructive transition-colors rounded-full hover:bg-muted"
            title="End Chat & Transcript"
            aria-label="End Chat"
          >
            <LogOut className="w-5 h-5" />
          </button>

          <div className="flex-1">
            <ChatInput onSend={handleSendMessage} isLoading={isLoading} />
          </div>
        </div>
      </div>
    </main>
  )
}
