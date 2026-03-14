// fuction to generate random pasword
function generateRandomPassword(lenght){
    const characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    let password = ''
    for(let i=0;i<lenght;i++){
      const lether = characters[Math.floor(Math.random(0,characters.length + 1)*100)]
      if(lether == undefined){
        i --
      }else{
        password += lether
      }
    }
    return password
  }

  // creates event listener for button to generate password and put on password textarea
  let passwordGenerateBtn = document.querySelector('#generatePassword')
  passwordGenerateBtn.addEventListener('click', function(){
    let passwordLength = document.querySelector('#passwordLength')
    const psw_len = Number(passwordLength.value)
    passwordLength.value = ''
    const generatedPassword = generateRandomPassword(psw_len)
    let usersPassword = document.querySelector('#user-password')
    usersPassword.value = generatedPassword
  })