const signinbtn = document.querySelector('#signinbtn');
const signupbtn= document.querySelector('#signupbtn');
const form_box = document.querySelector('.form-box');
let nameField = document.getElementById("nameField");
let confirm_pswd = document.getElementById("confirm_pswd");
let title = document.getElementById("title");
let rg = document.getElementById("registration");
let lg = document.getElementById("login");
let confirm_pswd_log = document.getElementById("confirm_pswd_log");
let nameField_log = document.getElementById("nameField_log");


let msglg = document.getElementById("msglg");
signinbtn.disabled = false;
signupbtn.disabled = false;

console.log("form_box.classList",form_box.classList)

if (msglg.value == "Invalid Credentials."){
    nameField.style.maxHeight = "0px";
    nameField_log.style.maxHeight = "0px";
    confirm_pswd.style.maxHeight= "0px";
    confirm_pswd_log.style.maxHeight = "0px";
    title.innerHTML = "Sign In";
    form_box.style.height = "310px";
    signupbtn.classList.add("disable1");
    signinbtn.classList.remove("disable1");
    form_box.classList.toggle("active");   
}
signinbtn.addEventListener('click', () => {
    nameField.style.maxHeight = "0px";
    nameField_log.style.maxHeight = "0px";
    confirm_pswd.style.maxHeight= "0px";
    confirm_pswd_log.style.maxHeight = "0px";
    title.innerHTML = "Sign In";
    form_box.style.height = "40%";
    signupbtn.classList.add("disable1");
    signinbtn.classList.remove("disable1");
    form_box.classList.toggle("active");
    if (signinbtn.disabled == false){
        signinbtn.disabled = true;
        signupbtn.disabled = false;
    }
});


signupbtn.addEventListener('click', () => {
    nameField.style.maxHeight = "65px";
    nameField_log.style.maxHeight = "65px";
    confirm_pswd.style.maxHeight= "65px";
    confirm_pswd_log.style.maxHeight = "65px";
    title.innerHTML = "Sign Up";
    form_box.style.height = "45%";
    signupbtn.classList.remove("disable1");
    signinbtn.classList.add("disable1");
    form_box.classList.toggle("active");
    if (signupbtn.disabled == false){
        signupbtn.disabled = true;
        signinbtn.disabled = false;
    }
});
    
