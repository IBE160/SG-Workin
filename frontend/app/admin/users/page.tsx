"use client"

import { useEffect, useState } from "react"
import { UserManager } from "@/components/admin/UserManager"
import { Button } from "@/components/ui/button"
import { createClient } from "@/utils/supabase/client"
import { useRouter } from "next/navigation"
import Link from "next/link"

export default function AdminUsersPage() {
    const router = useRouter()
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        const checkUser = async () => {
            const supabase = createClient()
            const { data } = await supabase.auth.getSession()
            if (!data.session) {
                router.push("/auth/login")
                return
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

    if (loading) return <div className="p-8">Loading user management...</div>

    return (
        <main className="container mx-auto p-8 max-w-5xl">
            <div className="flex justify-between items-center mb-8">
                <div className="flex items-center gap-4">
                    <h1 className="text-3xl font-bold">Admin: Users</h1>
                    <Link href="/admin">
                        <Button variant="outline">Back to Content</Button>
                    </Link>
                </div>
                <Button variant="outline" onClick={handleLogout}>Logout</Button>
            </div>
            <div className="grid grid-cols-1 gap-8">
                <UserManager />
            </div>
        </main>
    )
}
