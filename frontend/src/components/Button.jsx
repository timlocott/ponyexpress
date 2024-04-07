/* eslint-disable react/prop-types */
function Button(props) {
    return (
        <button {...props} className="p-2 border-britishRacingGreen border-2 rounded my-2 text-tomato hover:bg-tomato hover:text-britishRacingGreen w-fit">
            {props.children}
        </button>
    );
}

export default Button;