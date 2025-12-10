import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { ChatInput } from '../components/modules/chat/ChatInput'
import { ChatWindow } from '../components/modules/chat/ChatWindow'
import Page from '../app/page'

describe('Chat Interface', () => {
    it('renders the chat window layout', () => {
        render(<Page />)
        const chatWindow = screen.getByRole('main')
        expect(chatWindow).toBeDefined()
    })

    it('displays messages in ChatWindow', () => {
        const messages = [
            { role: 'user' as const, content: 'User Test' },
            { role: 'assistant' as const, content: 'Bot Test' }
        ]
        render(<ChatWindow messages={messages} />)

        expect(screen.getByText('User Test')).toBeDefined()
        expect(screen.getByText('Bot Test')).toBeDefined()
    })
})

describe('Chat Interaction', () => {
    it('calls onSend when send button is clicked', () => {
        const mockOnSend = vi.fn()
        render(<ChatInput onSend={mockOnSend} />)

        const input = screen.getByPlaceholderText('Type a message...') as HTMLInputElement
        const sendButton = screen.getByRole('button', { name: /send message/i })

        fireEvent.change(input, { target: { value: 'Hello' } })
        fireEvent.click(sendButton)

        expect(mockOnSend).toHaveBeenCalledWith('Hello')
    })

    it('integrates page state with api call', async () => {
        // Mock global fetch
        global.fetch = vi.fn().mockResolvedValue({
            ok: true,
            json: async () => ({
                status: 'success',
                data: { response: 'Mock Bot Response' }
            })
        })

        render(<Page />)

        const input = screen.getByPlaceholderText('Type a message...') as HTMLInputElement
        const sendButton = screen.getByRole('button', { name: /send message/i })

        // Send message
        fireEvent.change(input, { target: { value: 'Integration Test' } })
        fireEvent.click(sendButton)

        // Verify user message appears immediately
        await waitFor(() => {
            expect(screen.getByText('Integration Test')).toBeDefined()
        })

        // Verify API called
        expect(global.fetch).toHaveBeenCalledWith('http://127.0.0.1:8000/api/chat', expect.any(Object))

        // Verify bot response appears (after mock fetch resolves)
        await waitFor(() => {
            expect(screen.getByText('Mock Bot Response')).toBeDefined()
        })
    })
})
