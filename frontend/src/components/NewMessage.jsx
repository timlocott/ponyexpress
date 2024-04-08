/* eslint-disable react/prop-types */
import { useState } from "react";
import { useMutation, useQueryClient } from "react-query";
import { useNavigate } from "react-router-dom";
// import { useUser } from "../context/user";
import { useAuth } from "../context/auth";
import FormInput from "./FormInput";
import Button from "./Button";

function NewMessage({ chatId }){
    const [messageText, setMessageText] = useState("");

    // const user = useUser();
    const queryClient = useQueryClient();
    const navigate = useNavigate();
    const { token } = useAuth()

    const mutation = useMutation({
      mutationFn: () => (
        fetch(
          "http://127.0.0.1:8000/chats/" + chatId + "/messages",
          {
            method: "POST",

            headers: {
              "Authorization": "Bearer " + token,
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              messageText,
            }),
          },
        ).then((response) => response.json())
      ),
      // eslint-disable-next-line no-unused-vars
      onSuccess: (data) => {
        queryClient.invalidateQueries({
          queryKey: ["chats"],
        });
        navigate(`/chats/${chatId}`);
      },
    });

  const onSubmit = (e) => {
    e.preventDefault();
    mutation.mutate();
  };

    return (
        <div className="border-t border-vanilla px-6">
            <form onSubmit={onSubmit} className="flex grow flex-row justify-between">
                <FormInput type="text" setter={setMessageText} />
                <Button type="submit">send</Button>
            </form>
        </div>
    );
}

export default NewMessage;