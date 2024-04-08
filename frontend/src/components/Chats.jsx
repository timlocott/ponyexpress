/* eslint-disable react/prop-types */
import { useQuery } from "react-query";
import { Link, useParams } from "react-router-dom";
import NewMessage from "./NewMessage";
// import "./Chats.css";

function ChatListItem({ chat }) {
    return (
        <Link key={chat.id} to={`/chats/${chat.id}`} className="mx-1.5 p-3 hover:bg-wenge hover:text-vanilla se">
            <div className="font-bold">
                {chat.name}
            </div>
        </Link>
    )

}

function ChatList({ chats }) {
    return (
        <div className="flex flex-col">
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
        <div className="flex flex-col grow-0 shrink-0 w-max bg-vanilla max-h-[95vh] h-[95vh]">
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
            <div>
                <div>
                    <MessageList messages={data.messages} />
                </div>
                <NewMessage chatId={chat.id} />
            </div>
        )
    }

    return (
        <h2>loading...</h2>
    );
}

function ChatCardContainer({ chat }) {
    return (
        <div className="flex flex-row grow justify-center max-h-[98vh] h-[98vh]">
                <div className="">
                    <ChatCard chat={chat} />
                </div>
        </div>
    )
}

function ChatCardQueryContainer({ chatId }){
    if (!chatId) {
        return (
            <div className="flex flex-col">
                <h3 className="ml-14 mt-10 text-verdigris">Select a chat</h3>
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

    return <h2 className="ml-14 mt-10 text-verdigris">loading...</h2>
}

function MessageList({ messages }) {
    return (
        <div className="flex mx-2.5 my-4 p-2.5 overflow-y-scroll flex-col max-h-[84vh] h-[84vh]">
            {messages.map((message) => (
                <MessageListItem key={message.id} message={message} />
            ))}
        </div>
    )
}

function MessageListItem({ message }) {
    return (
        <div key={message.id} className="m-1.5 p-2.5 border border-britishRacingGreen">
            <div className="flex flex-row justify-between">
                <div className="font-bold text-sm mr-2.5 text-verdigris">
                    {message.user.username}
                </div>
                <div className="text-xs font-extralight text-beige">
                    {new Date(message.created_at).toDateString()} - {new Date(message.created_at).toLocaleTimeString()}
                </div>
            </div>
            <div className="my-2.5 ml-2.5 font-extralight text-m text-tomato">
                {message.text}
            </div>
        </div>
    )
}

function Chats() {
    const { chatId } = useParams();
    if (!chatId){
        return (
        <div className="flex grow flex-row justify-start">
            <ChatListContainer />
            <ChatCardQueryContainer chatId={chatId} />
        </div>
    );
    }
    return (
        <div className="flex grow flex-row justify-between">
            <ChatListContainer />
            <ChatCardQueryContainer chatId={chatId} />
        </div>
    );
}

export default Chats;