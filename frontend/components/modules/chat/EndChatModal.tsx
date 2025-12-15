
"use client"

import { useState } from "react"
import { Star, Mail, X } from "lucide-react"

interface EndChatModalProps {
    onSubmit: (score: number, comment: string, email: string) => Promise<void>
    onClose: () => void
}

export function EndChatModal({ onSubmit, onClose }: EndChatModalProps) {
    const [score, setScore] = useState<number>(0)
    const [comment, setComment] = useState("")
    const [email, setEmail] = useState("")
    const [isSubmitting, setIsSubmitting] = useState(false)
    const [submitted, setSubmitted] = useState(false)

    const handleSubmit = async () => {
        // Rating optional or mandatory? Let's make rating mandatory for "Feedback", 
        // but if they just want email, maybe allow it? 
        // PRD says "end of conversation" usually implies feedback. 
        // Let's keep rating mandatory to encourage data.
        if (score === 0) return

        setIsSubmitting(true)
        await onSubmit(score, comment, email)
        setIsSubmitting(false)
        setSubmitted(true)
        setTimeout(onClose, 3000)
    }

    if (submitted) {
        return (
            <div className="p-6 text-center bg-background rounded-lg shadow-xl border w-full max-w-sm">
                <h3 className="text-xl font-medium text-green-600 mb-2">Thank you!</h3>
                <p className="text-muted-foreground text-sm">
                    {email ? "Transcript sent and chat ended." : "Feedback received. Chat ended."}
                </p>
            </div>
        )
    }

    return (
        <div className="p-6 bg-background border rounded-lg shadow-xl max-w-sm w-full relative">
            <button onClick={onClose} className="absolute top-4 right-4 text-muted-foreground hover:text-foreground">
                <X className="w-4 h-4" />
            </button>

            <h3 className="text-lg font-bold mb-1">End Chat Session</h3>
            <p className="text-xs text-muted-foreground mb-4">Rate your experience to close the session.</p>

            {/* Rating */}
            <div className="flex gap-2 justify-center mb-4">
                {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((num) => (
                    <button
                        key={num}
                        onClick={() => setScore(num)}
                        className={`w-8 h-8 rounded-full flex items-center justify-center text-sm transition-all duration-200
                            ${score >= num
                                ? "bg-yellow-400 text-white scale-110"
                                : "bg-muted text-muted-foreground hover:bg-muted/80"}`}
                        title={`${num} Stars`}
                    >
                        {num}
                    </button>
                ))}
            </div>

            {/* Comment */}
            <textarea
                className="w-full p-2 border rounded-md mb-4 bg-background text-foreground text-sm focus:ring-2 focus:ring-primary/20 outline-none transition-all"
                placeholder="Any comments? (Optional)"
                rows={3}
                value={comment}
                onChange={(e) => setComment(e.target.value)}
            />

            {/* Email Transcript */}
            <div className="mb-6">
                <div className="flex items-center gap-2 mb-2 text-sm font-medium">
                    <Mail className="w-4 h-4" />
                    <span>Get Transcript (Optional)</span>
                </div>
                <input
                    type="email"
                    placeholder="Enter your email address"
                    className="w-full p-2 border rounded-md bg-background text-foreground text-sm focus:ring-2 focus:ring-primary/20 outline-none transition-all"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
            </div>

            <div className="flex justify-end gap-2">
                <button
                    onClick={onClose}
                    className="px-4 py-2 text-sm text-muted-foreground hover:text-foreground"
                >
                    Cancel
                </button>
                <button
                    onClick={handleSubmit}
                    disabled={score === 0 || isSubmitting}
                    className="px-4 py-2 text-sm bg-destructive text-destructive-foreground hover:bg-destructive/90 rounded-md disabled:opacity-50 transition-colors"
                >
                    {isSubmitting ? "Ending..." : "End Chat"}
                </button>
            </div>
        </div>
    )
}
