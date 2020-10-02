const username=document.querySelector('#username')
const userFeedback=document.querySelector(".user-feedback")
const email=document.querySelector('#email')
const emailFeedback=document.querySelector(".email-feedback")
const usernameSuccessOutput=document.querySelector(".usernameSuccessOutput")
const password=document.querySelector("#password")
const showPasswordToggle=document.querySelector(".showPasswordToggle")

const handleToggleInput=(e)=>{
    if(showPasswordToggle.textContent==="Show"){
        showPasswordToggle.textContent="Hide"
        password.setAttribute("type","text")
    }else {
        showPasswordToggle.textContent="Show"
        password.setAttribute("type","password")
    }
}

showPasswordToggle.addEventListener('click',handleToggleInput)


username.addEventListener("keyup",(e)=>{

    const usernameValue=e.target.value;
    usernameSuccessOutput.textContent=`Checking ${usernameValue}`

    username.classList.remove("is-invalid")
    userFeedback.style.display="none";
    if(usernameValue.length>0){
        fetch("/authentication/validate-username/",{
            method:"POST",
            body:JSON.stringify({username:usernameValue})
        }).then((res)=>res.json())
            .then((data)=>{
            console.log("data",data)
            usernameSuccessOutput.style.display="none"
            if(data.username_error){
                username.classList.add("is-invalid")
                userFeedback.style.display="block";
                userFeedback.innerHTML=`<p>${data.username_error}</p>`
            }
        })
    }
})

email.addEventListener("keyup",(e)=>{
    const emailValue=e.target.value

    email.classList.remove('is-invalid')
    emailFeedback.style.display="none"
    if(emailValue.length>0){
        fetch("/authentication/validate-email/",{
            method:"POST",
            body:JSON.stringify({email:emailValue})
        }).then((res)=>res.json())
        .then((data)=>{
            if(data.email_error){
                email.classList.add('is-invalid')
                emailFeedback.style.display="block"
                emailFeedback.innerHTML=`<p>${data.email_error}</p>`
            }
        })

    }

})