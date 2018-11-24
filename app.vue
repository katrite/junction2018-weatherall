
<template>
  <div id="app">
  </div>
</template>
<script>
// import GroupInfoContainer from './components/group-info/group-info-container';

export default {
  name: 'App',
  store,
  components: {
    // 'group-info': GroupInfoContainer,

  },
  computed: {
    groupExists() {
      return this.groupMembers && this.groupMembers.length > 0;
    },
  },
  methods: {
    isOnlyAdult() {
      const groupAdults = this.groupMembers.filter(user => user.juniorFlag === 'N');
      return this.groupMembers.length === 1 || groupAdults.length === 1;
    },
  },
  created() {
    if (!store.state.groupInfo || !store.state.groupInfo.length) {
      store.dispatch('START_LOADING_GROUP_DATA');
    }
  },
};
</script>

