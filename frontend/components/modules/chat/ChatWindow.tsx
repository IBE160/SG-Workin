export interface Message {
    role: 'user' | 'assistant'
    content: string
}

interface ChatWindowProps {
    messages: Message[]
}

export function ChatWindow({ messages }: ChatWindowProps) {
    return (
        <div className="flex-1 w-full max-w-5xl p-4 overflow-y-auto mb-20 rounded-lg border bg-card text-card-foreground shadow-sm">
            <div className="flex flex-col gap-4">
                {messages.map((msg, idx) => (
                    <div
                        key={idx}
                        className={`flex w-max max-w-[75%] flex-col gap-2 rounded-lg px-3 py-2 text-sm ${msg.role === 'user'
                                ? "ml-auto bg-primary text-primary-foreground"
                                : "bg-muted text-muted-foreground self-start"
                            }`}
                    >
                        {msg.content}
                    </div>
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
