"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { createClient } from "@/utils/supabase/client"

interface User {
    id: string
    email: string
    created_at?: string
    last_sign_in_at?: string
}

export function UserManager() {
    const [users, setUsers] = useState<User[]>([])
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [loading, setLoading] = useState(false)
    const [message, setMessage] = useState("")

    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000/api'

    const getAuthHeaders = async () => {
        const supabase = createClient()
        const { data } = await supabase.auth.getSession()
        return {
            "Content-Type": "application/json",
            "Authorization": data.session?.access_token ? `Bearer ${data.session.access_token}` : ""
        }
    }

    useEffect(() => {
        fetchUsers()
    }, [])

    const fetchUsers = async () => {
        try {
            const headers = await getAuthHeaders()
            const res = await fetch(`${apiUrl}/admin/users`, { headers })
            if (res.ok) {
                const data = await res.json()
                if (Array.isArray(data)) setUsers(data)
                else if (data.users && Array.isArray(data.users)) setUsers(data.users)
                else setUsers([])
            } else {
                console.error("Fetch users failed", res.status)
            }
        } catch (e) {
            console.error("Fetch users error", e)
        }
    }

    const addUser = async () => {
        setLoading(true)
        setMessage("")
        try {
            const headers = await getAuthHeaders()
            const res = await fetch(`${apiUrl}/admin/users`, {
                method: "POST",
                headers,
                body: JSON.stringify({ email, password })
            })
            const data = await res.json()
            if (res.ok) {
                setMessage("User added successfully!")
                setEmail("")
                setPassword("")
                fetchUsers()
            } else {
                setMessage("Error adding user: " + data.detail)
            }
        } catch (e) {
            setMessage("Error: " + e)
        } finally {
            setLoading(false)
        }
    }

    const deleteUser = async (id: string, email: string) => {
        if (!confirm(`Delete user ${email}?`)) return
        try {
            const headers = await getAuthHeaders()
            const res = await fetch(`${apiUrl}/admin/users/${id}`, {
                method: "DELETE",
                headers
            })
            if (res.ok) fetchUsers()
            else {
                const data = await res.json()
                alert("Failed to delete: " + data.detail)
            }
        } catch (e) {
            alert("Error deleting: " + e)
        }
    }

    const resetPassword = async (email: string) => {
        if (!confirm(`Send password reset email to ${email}?`)) return
        try {
            const headers = await getAuthHeaders()
            const res = await fetch(`${apiUrl}/admin/users/reset-password`, {
                method: "POST",
                headers,
                body: JSON.stringify({ email })
            })
            const data = await res.json()
            alert(data.message || data.detail)
        } catch (e) {
            alert("Error resetting password: " + e)
        }
    }

    return (
        <Card>
            <CardHeader>
                <CardTitle>User Management</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
                <div className="space-y-4 border p-4 rounded bg-slate-50">
                    <h3 className="font-semibold text-sm">Add New Admin</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <Label htmlFor="email">Email</Label>
                            <Input id="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="admin@example.com" />
                        </div>
                        <div>
                            <Label htmlFor="pass">Password</Label>
                            <Input id="pass" type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="StrongPassword123" />
                        </div>
                    </div>
                    <Button onClick={addUser} disabled={loading || !email || !password}>
                        {loading ? "Adding..." : "Add Admin"}
                    </Button>
                    {message && <p className="text-sm text-gray-600">{message}</p>}
                </div>

                <div>
                    <h3 className="font-semibold mb-2">Existing Admins ({users.length})</h3>
                    <div className="border rounded divide-y max-h-[300px] overflow-y-auto">
                        {users.length === 0 && <p className="p-4 text-sm text-gray-500">No users found.</p>}
                        {users.map(u => (
                            <div key={u.id} className="p-3 flex justify-between items-center hover:bg-slate-50">
                                <div className="overflow-hidden">
                                    <p className="font-medium truncate" title={u.email}>{u.email}</p>
                                    <p className="text-xs text-gray-400 font-mono truncate w-full max-w-[200px]" title={u.id}>ID: {u.id}</p>
                                    {u.last_sign_in_at && <p className="text-xs text-gray-400">Last seen: {new Date(u.last_sign_in_at).toLocaleDateString()}</p>}
                                </div>
                                <div className="flex gap-2">
                                    <Button variant="outline" size="sm" onClick={() => resetPassword(u.email)}>Reset Pwd</Button>
                                    <Button variant="destructive" size="sm" onClick={() => deleteUser(u.id, u.email)}>Delete</Button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </CardContent>
        </Card>
    )
}
