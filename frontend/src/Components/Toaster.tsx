import "./toastter_style.css"

interface props_toaster{
    message: string
}

const MessageType = {
    LOG: {color: "white", banner: "[LOG]"},
    ERROR: {color: "red", banner: "[ERROR]"},
    WARNING: {color: "yellow", banner: "[WARNING]"},
    WORKING: {color: "lightblue", banner: "[WORKING]"},
    HINT: {color: "white", banner: "[HINT]"},
} as const

type MessageTypeKey = keyof typeof MessageType;

function ShowToaster(){
    const toaster = document.querySelector('.toaster') as HTMLElement;
    if(toaster){
        toaster.classList.remove('toaster-hide');
    }
  }

  function SetMessage(type: MessageTypeKey, message: string){
    const toaster_body = document.querySelector('.toaster-body') as HTMLElement;
    toaster_body.innerHTML = `<span style="color:${MessageType[type].color}"> ${MessageType[type].banner}</span>${message}`
  }

  function CloseToaster(){
    const toaster = document.querySelector('.toaster') as HTMLElement;
    if(toaster){
        toaster.classList.add('toaster-hide');
    }
  }

function Toaster(props: props_toaster){
    return (
        <div onClick={CloseToaster} className="toaster toaster-hide">
            <div className="toaster-main">
                
                <div className="toaster-body">
                {props.message}
                </div>
            </div>
        </div>
    )
}

export {Toaster, SetMessage, ShowToaster, CloseToaster, MessageType};
export type {MessageTypeKey};