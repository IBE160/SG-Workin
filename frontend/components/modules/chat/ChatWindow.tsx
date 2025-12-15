import { ChatMessageItem } from "./ChatMessageItem"

export interface Message {
    role: 'user' | 'assistant'
    content: string
    type?: 'answer' | 'clarification' | 'escalation'
    escalationLink?: string
    sources?: string[]
}

interface ChatWindowProps {
    messages: Message[]
}

export function ChatWindow({ messages }: ChatWindowProps) {
    return (
        <div className="flex-1 w-full max-w-5xl p-4 overflow-y-auto mb-20 rounded-lg border bg-card text-card-foreground shadow-sm">
            <div className="flex flex-col gap-4">
                {messages.map((msg, idx) => (
                    <ChatMessageItem key={idx} message={msg} />
                ))}
                {messages.length === 0 && (
                    <div className="text-center text-muted-foreground mt-10">
                        No messages yet. Say hi!
                    </div>
                )}
            </div>
        </div>
    )
}
