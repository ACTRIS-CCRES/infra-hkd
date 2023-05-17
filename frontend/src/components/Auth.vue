
<template>
  <div>
    <button @click="handleClick">
      <span>Connect with Keycloak</span>
      <img src="../assets/keycloak.png" alt="Keycloak Logo">
    </button>

  </div>
</template>

<script setup lang="ts">

let BASE_URL = "https://sso.aeris-data.fr/auth/realms/auth/protocol/openid-connect/auth"
let REDIRECT_URI = "http%3A%2F%2Flocalhost%3A5173%2F"
let CLIENT_ID = "grafana"
let SCOPES = "email+profile+openid"
let RESPONSE_TYPE = "code"
let STATE = "WyhSk9H9DrLj"


function handleClick() {
  let url = `${BASE_URL}?client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&scope=${SCOPES}&response_type=${RESPONSE_TYPE}&state=${STATE}`
  window.location.href = url
}
</script>
<style scoped>
button {
  display: flex;
  padding: 3px 5px;
  background-color: white;
  justify-content: center;
  align-items: center;
  border: solid 1px grey;
  border-radius: 20px;
  cursor: pointer;
}

button span {
  font-size: 16px;
  font-weight: 400;
}

button img {
  width: 35px;
}
</style>
