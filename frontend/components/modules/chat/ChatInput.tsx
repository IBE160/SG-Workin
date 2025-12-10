"use client"

import { Send } from "lucide-react"
import { useState } from "react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

interface ChatInputProps {
    onSend: (message: string) => void
    isLoading?: boolean
}

export function ChatInput({ onSend, isLoading }: ChatInputProps) {
    const [message, setMessage] = useState("")

    const handleSend = () => {
        if (!message.trim() || isLoading) return

        onSend(message)
        setMessage("")
    }

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            handleSend()
        }
    }

    return (
        <div className="relative flex items-center w-full gap-2">
            <Input
                placeholder="Type a message..."
                aria-label="Chat input"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyDown={handleKeyDown}
                disabled={isLoading}
            />
            <Button
                size="icon"
                aria-label="Send message"
                onClick={handleSend}
                disabled={isLoading || !message.trim()}
            >
                <Send className="h-4 w-4" />
            </Button>
        </div>
    )
}
