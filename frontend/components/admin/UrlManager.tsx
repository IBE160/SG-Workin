"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { createClient } from "@/utils/supabase/client"

interface ScrapedUrl {
    url: string
    title: string
    scraped_at: string
}

export function UrlManager() {
    // State
    const [urls, setUrls] = useState<ScrapedUrl[]>([])
    const [newUrl, setNewUrl] = useState("")
    const [loading, setLoading] = useState(false)
    const [message, setMessage] = useState("")
    const [searchTerm, setSearchTerm] = useState("")
    const [sortField, setSortField] = useState<"url" | "title" | "scraped_at">("scraped_at")
    const [sortOrder, setSortOrder] = useState<"asc" | "desc">("desc")

    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000/api'

    // Auth Helper
    const getAuthHeaders = async () => {
        const supabase = createClient()
        const { data } = await supabase.auth.getSession()
        return {
            "Content-Type": "application/json",
            "Authorization": data.session?.access_token ? `Bearer ${data.session.access_token}` : ""
        }
    }

    // Initial Fetch
    useEffect(() => {
        fetchUrls()
    }, [])

    const fetchUrls = async () => {
        try {
            const headers = await getAuthHeaders()
            const res = await fetch(`${apiUrl}/admin/urls`, { headers })
            if (res.ok) {
                const data = await res.json()
                setUrls(data)
            }
        } catch (e) {
            console.error("Failed to fetch URLs", e)
        }
    }

    // Actions
    const triggerScrape = async (url: string) => {
        const headers = await getAuthHeaders()
        const res = await fetch(`${apiUrl}/admin/scrape`, {
            method: "POST",
            headers,
            body: JSON.stringify({ url })
        })
        const data = await res.json()
        if (res.ok) {
            setTimeout(fetchUrls, 2000)
        } else {
            throw new Error(data.detail)
        }
    }

    const handleScrape = async () => {
        if (!newUrl) return
        setLoading(true)
        setMessage("")
        try {
            await triggerScrape(newUrl)
            setMessage("Scraping started!")
            setNewUrl("")
        } catch (e: any) {
            setMessage("Error: " + e.message)
        } finally {
            setLoading(false)
        }
    }

    const deleteUrl = async (url: string) => {
        if (!confirm(`Delete all content for ${url}?`)) return
        try {
            const headers = await getAuthHeaders()
            const res = await fetch(`${apiUrl}/admin/urls?url=${encodeURIComponent(url)}`, {
                method: "DELETE",
                headers
            })
            if (res.ok) fetchUrls()
            else {
                const data = await res.json()
                alert("Failed to delete: " + data.detail)
            }
        } catch (e) {
            alert("Error deleting: " + e)
        }
    }

    const rescrapeUrl = async (url: string) => {
        if (!confirm(`Rescrape ${url}?`)) return
        try {
            await triggerScrape(url)
            alert("Rescrape started for " + url)
        } catch (e: any) {
            alert("Error rescraping: " + e.message)
        }
    }

    const deleteAllData = async () => {
        const input = prompt("Type 'delete' to confirm DELETING ALL SCRAPED DATA. This cannot be undone.")
        if (input !== "delete") {
            if (input !== null) alert("Deletion cancelled. Keyword did not match.")
            return
        }

        try {
            const headers = await getAuthHeaders()
            const res = await fetch(`${apiUrl}/admin/scrape/all`, {
                method: "DELETE",
                headers
            })
            if (res.ok) {
                alert("All data deleted.")
                fetchUrls()
            } else {
                const data = await res.json()
                alert("Failed to delete all data: " + data.detail)
            }
        } catch (e: any) {
            alert("Error deleting all data: " + e.message)
        }
    }

    // Filter & Sort Logic
    const toggleSort = (field: "url" | "title" | "scraped_at") => {
        if (sortField === field) {
            setSortOrder(sortOrder === "asc" ? "desc" : "asc")
        } else {
            setSortField(field)
            setSortOrder("asc")
        }
    }

    const filteredAndSortedUrls = urls
        .filter(u =>
            u.url.toLowerCase().includes(searchTerm.toLowerCase()) ||
            (u.title && u.title.toLowerCase().includes(searchTerm.toLowerCase()))
        )
        .sort((a, b) => {
            const fieldA = a[sortField] || ""
            const fieldB = b[sortField] || ""
            if (fieldA < fieldB) return sortOrder === "asc" ? -1 : 1
            if (fieldA > fieldB) return sortOrder === "asc" ? 1 : -1
            return 0
        })

    return (
        <Card>
            <CardHeader>
                <CardTitle>Content Management</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
                {/* Input Section */}
                <div className="flex gap-2 items-end">
                    <div className="grid w-full max-w-sm items-center gap-1.5">
                        <Label htmlFor="url">Add URL to Scrape</Label>
                        <Input
                            type="url"
                            id="url"
                            placeholder="https://www.himolde.no/..."
                            value={newUrl}
                            onChange={(e) => setNewUrl(e.target.value)}
                        />
                    </div>
                    <Button onClick={handleScrape} disabled={loading}>
                        {loading ? "Scraping..." : "Scrape"}
                    </Button>
                </div>
                {message && <p className="text-sm text-gray-500">{message}</p>}

                {/* List Section */}
                <div className="border rounded-md p-4 bg-white">
                    <div className="flex justify-between items-center mb-4">
                        <h3 className="font-semibold">Active URLs ({urls.length})</h3>
                        <div className="flex gap-2">
                            <Button variant="destructive" size="sm" onClick={deleteAllData}>Delete All Data</Button>
                            <Input
                                placeholder="Search title or url..."
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                                className="max-w-[250px]"
                            />
                        </div>
                    </div>

                    <div className="divide-y max-h-[500px] overflow-y-auto">
                        {/* Headers */}
                        <div className="flex text-xs font-bold text-gray-500 py-2 px-2 bg-slate-100 rounded-t sticky top-0 z-10">
                            <div className="flex-1 cursor-pointer hover:text-black flex items-center gap-1" onClick={() => toggleSort("title")}>
                                Title / URL {sortField === "title" && (sortOrder === "asc" ? "↑" : "↓")}
                            </div>
                            <div className="w-[120px] cursor-pointer hover:text-black flex items-center gap-1 hidden md:flex" onClick={() => toggleSort("scraped_at")}>
                                Date {sortField === "scraped_at" && (sortOrder === "asc" ? "↑" : "↓")}
                            </div>
                            <div className="w-[150px] text-right pr-2">Actions</div>
                        </div>

                        {/* Items */}
                        {filteredAndSortedUrls.length === 0 && <p className="text-sm text-gray-400 p-4 text-center">No URLs found.</p>}
                        {filteredAndSortedUrls.map((u) => (
                            <div key={u.url} className="flex justify-between items-center text-sm py-3 border-b last:border-0 hover:bg-slate-50 px-2 group transition-colors">
                                <div className="overflow-hidden mr-2 flex-1">
                                    <a href={u.url} target="_blank" className="text-blue-600 hover:underline truncate block font-medium group-hover:text-blue-800" title={u.title || u.url}>
                                        {u.title || "Untitled"}
                                    </a>
                                    <p className="text-xs text-gray-400 truncate mt-0.5">{u.url}</p>
                                    <p className="text-xs text-gray-400 md:hidden mt-0.5">
                                        {u.scraped_at ? new Date(u.scraped_at).toLocaleString([], { dateStyle: 'short', timeStyle: 'short' }) : 'N/A'}
                                    </p>
                                </div>
                                <div className="w-[120px] text-xs text-gray-500 hidden md:block">
                                    {u.scraped_at ? new Date(u.scraped_at).toLocaleString([], { dateStyle: 'short', timeStyle: 'short' }) : 'N/A'}
                                </div>
                                <div className="flex gap-2 w-[150px] justify-end opacity-60 group-hover:opacity-100 transition-opacity">
                                    <Button variant="outline" size="sm" className="h-8" onClick={() => rescrapeUrl(u.url)}>Update</Button>
                                    <Button variant="destructive" size="sm" className="h-8" onClick={() => deleteUrl(u.url)}>Delete</Button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </CardContent>
        </Card>
    )
}
