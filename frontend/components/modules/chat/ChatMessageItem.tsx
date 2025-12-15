
import { Message } from "./ChatWindow"
import { BookOpen, ExternalLink, ChevronDown, ChevronUp } from "lucide-react"
import { useState } from "react"

import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"

interface ChatMessageItemProps {
    message: Message
}

export function ChatMessageItem({ message }: ChatMessageItemProps) {
    const isUser = message.role === 'user'
    const [showSources, setShowSources] = useState(false)

    return (
        <div
            className={`flex w-max max-w-[85%] flex-col gap-2 rounded-lg px-4 py-3 text-sm ${isUser
                ? "ml-auto bg-primary text-primary-foreground"
                : "bg-muted text-muted-foreground self-start"
                }`}
        >
            <div className="leading-relaxed prose prose-sm dark:prose-invert max-w-none break-words">
                <ReactMarkdown
                    remarkPlugins={[remarkGfm]}
                    components={{
                        a: ({ node, ...props }) => (
                            <a {...props} target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline font-medium" />
                        ),
                        p: ({ node, ...props }) => <p {...props} className="mb-2 last:mb-0" />,
                        ul: ({ node, ...props }) => <ul {...props} className="list-disc pl-4 mb-2" />,
                        ol: ({ node, ...props }) => <ol {...props} className="list-decimal pl-4 mb-2" />
                    }}
                >
                    {message.content}
                </ReactMarkdown>
            </div>

            {/* Collapsible Sources */}
            {message.sources && message.sources.length > 0 && (
                <div className="mt-1 pt-1 border-t border-border/20">
                    <button
                        onClick={() => setShowSources(!showSources)}
                        className="flex items-center gap-2 text-xs font-semibold opacity-70 hover:opacity-100 transition-opacity w-full text-left py-1"
                    >
                        <BookOpen className="w-3 h-3" />
                        <span>Sources ({message.sources.length})</span>
                        {showSources ? <ChevronUp className="w-3 h-3 ml-auto" /> : <ChevronDown className="w-3 h-3 ml-auto" />}
                    </button>

                    {showSources && (
                        <ul className="mt-2 space-y-2 animate-in fade-in slide-in-from-top-1">
                            {message.sources.map((source, idx) => (
                                <li key={idx} className="flex text-xs bg-background/50 p-2 rounded hover:bg-background/80 transition-colors">
                                    <ExternalLink className="w-3 h-3 min-w-[12px] mt-0.5 mr-2" />
                                    <a
                                        href={source}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="text-blue-500 hover:underline break-all"
                                    >
                                        {source}
                                    </a>
                                </li>
                            ))}
                        </ul>
                    )}
                </div>
            )}

            {message.type === 'escalation' && message.escalationLink && (
                <div className="mt-2 p-3 bg-background/50 rounded border border-border/20">
                    <p className="text-sm font-medium mb-1">Need more help?</p>
                    <a
                        href={message.escalationLink}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-500 hover:underline text-sm flex items-center gap-1"
                    >
                        Contact Support ↗
                    </a>
                </div>
            )}
        </div>
    )
}
