<template>
    <nav class="wrapper">
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/bashos">Basho</RouterLink>
      <RouterLink to="">Current basho</RouterLink>
    </nav>
</template>

<style>
.wrapper {
  background-color: #d8c7b2;
  display: flex;
  justify-content: space-around;
}

.wrapper * {
  padding: 2%;
}

.wrapper *:hover {
  background-color: #4d4740;
  border-radius: 5px;
}
</style>