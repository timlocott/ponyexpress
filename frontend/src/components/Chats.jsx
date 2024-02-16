/* eslint-disable react/prop-types */
import { useQuery } from "react-query";
import { Link, useParams } from "react-router-dom";
import "./Chats.css";

function ChatListItem({ chat }) {
    return (
        <Link key={chat.id} to={`/chats/${chat.id}`} className="chat-list-item">
            <div className="chat-list-item-name">
                {chat.name}
            </div>
            <div className="chat-list-item-userIds">
                {chat.user_ids.join(", ")}
            </div>
            <div className="chat-list-item-datetime">
                Created on: {new Date(chat.created_at).toDateString()}
            </div>
        </Link>
    )

}

function ChatList({ chats }) {
    return (
        <div className="chat-list">
            {chats.map((chat) => (
                <ChatListItem key={chat.id} chat={chat} />
            ))}
        </div>
    )
}

function ChatListContainer() {
    const { data } = useQuery({
        queryKey: ["chats"],
        queryFn: () => (
        fetch("http://127.0.0.1:8000/chats")
            .then((response) => response.json())
        ),
    });

    if (data?.chats) {
        return (
        <div className="chat-list-container">
            <h2>Chats</h2>
            <ChatList chats={data.chats} />
        </div>
        )
    }

    return (
        <h2>Chat List</h2>
    );
}

function ChatCard({ chat }) {
    const { data } = useQuery({
        queryKey: ["messages", chat.id],
        queryFn: () => (
        fetch(`http://127.0.0.1:8000/chats/${chat.id}/messages`)
            .then((response) => response.json())
        ),
    });

    if (data?.messages) {
        return (
        <div className="chat-card">
            <MessageList messages={data.messages} />
        </div>
        )
    }

    return (
        <h2 className="chat-card">loading...</h2>
    );
}

function ChatCardContainer({ chat }) {
    return (
        <div className="container-margin-sides">
                <h2> {chat.name} </h2>
                <div className="chat-card-container">
                    <ChatCard chat={chat} />
                </div>
        </div>
    )
}

function ChatCardQueryContainer({ chatId }){
    if (!chatId) {
        return (
            <div className="container-margin-sides">
                <h2> Messages </h2>
                <h3>Select a chat</h3>
            </div>
        );
    }

    const { data } = useQuery({
        queryKey: ["chats", chatId],
        queryFn: () => (
            fetch(`http://127.0.0.1:8000/chats/${chatId}`)
                .then((response) => response.json())
        ),
    });

    if (data && data.chat) {
        return <ChatCardContainer chat={data.chat} />
    }

    return <h2>loading...</h2>
}

function MessageList({ messages }) {
    return (
        <div className="message-list">
            {messages.map((message) => (
                <MessageListItem key={message.id} message={message} />
            ))}
        </div>
    )
}

function MessageListItem({ message }) {
    return (
        <div key={message.id} className="message-list-item">
            <div className="message-detail">
                <div className="message-list-item-userid">
                    {message.user_id}
                </div>
                <div className="message-list-item-datetime">
                    {new Date(message.created_at).toDateString()} - {new Date(message.created_at).toLocaleTimeString()}
                </div>
            </div>
            <div className="message-list-item-text">
                {message.text}
            </div>
        </div>
    )
}

function Chats() {
    const { chatId } = useParams();
    return (
        <div className="chats-page">
            <h1 className="title">PONY EXPRESS</h1>
            <ChatListContainer />
            <ChatCardQueryContainer chatId={chatId} />
        </div>
    );
}

export default Chats;