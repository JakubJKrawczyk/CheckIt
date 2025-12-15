
function ShowToaster(Message: string){
    const toaster = document.querySelector('.toaster') as HTMLElement;
    if(toaster){
        toaster.innerText = Message;
        toaster.classList.remove('toaster-hide');
        setTimeout(() => {
            toaster.classList.add('toaster-hide');
        }, 3000);
    }
  }


function Toaster(Message: string){
    return (
        <div className="toaster toaster-hide">
            {Message}
        </div>
    )
}

export {Toaster, ShowToaster};