"use client"

import { useEffect, useState } from "react"
import { UrlManager } from "@/components/admin/UrlManager"
import { Button } from "@/components/ui/button"
import { createClient } from "@/utils/supabase/client"
import { useRouter } from "next/navigation"
import Link from "next/link"

export default function AdminPage() {
    const router = useRouter()
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        const checkUser = async () => {
            const supabase = createClient()
            const { data } = await supabase.auth.getSession()
            if (!data.session) {
                router.push("/auth/login")
                return // Prevent loading state change
            }
            setLoading(false)
        }
        checkUser()
    }, [router])

    const handleLogout = async () => {
        const supabase = createClient()
        await supabase.auth.signOut()
        router.push("/auth/login")
    }

    if (loading) return <div className="p-8">Loading content manager...</div>

    return (
        <main className="container mx-auto p-8 max-w-5xl">
            <div className="flex justify-between items-center mb-8">
                <div className="flex items-center gap-4">
                    <h1 className="text-3xl font-bold">Admin: Content</h1>
                    <Link href="/admin/users">
                        <Button variant="outline">Manage Users</Button>
                    </Link>
                </div>
                <Button variant="outline" onClick={handleLogout}>Logout</Button>
            </div>
            <div className="grid grid-cols-1 gap-8">
                <UrlManager />
            </div>
        </main>
    )
}
