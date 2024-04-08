/* eslint-disable react/prop-types */
function FormInput({ setter, ...props}){
    let onChange;
    if (props.onChange) {
        onChange = props.onChange;
    } else if (setter) {
        onChange = (e) => setter(e.target.value);
    } else {
        onChange = () => {};
    }

    return (
        <div className="flex grow flex-col my-2 mr-2 justify-center">
            <label htmlFor={props.name} className="text-verdigris">{props.name}</label>
            <input {...props} onChange={onChange} className="text-black p-1"/>
        </div>
    );
}

export default FormInput;