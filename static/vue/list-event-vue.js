var vueapp = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        events: [],
        err_messages: [],
        _before_edit: new Object()
    },
    created () {
        this.api_call('http://localhost:8000/api/event/?format=json','GET')
        .then(response => {
            response.data.forEach(item => {
                Object.assign(item,{'edit':false});
                Object.assign(item,{'detail':false});
                Object.assign(item,{'card_view':true});
                this.events.push(item);
            });
        })
    },
    methods: {
        event_detail: function(event){
            console.log(''.concat('event_detail ',event.name))
            this.invert_detail(event)
            this.invert_card_view()
        },
        invert_detail: function(event){
            var new_events_array = []
            this.events.forEach(item => {
                if (item.id == event.id){
                    console.log("set detail to " + !item.detail + ", event_id: " + item.id)
                    item.detail = !item.detail;
                }
                new_events_array.push(item)
            });
            this.events = new_events_array
            delete new_events_array
        },
        invert_card_view: function(){
            var new_events_array = []
            this.events.forEach(item => {
                item.card_view = !item.card_view
                new_events_array.push(item)
            });
            this.events = new_events_array
            delete new_events_array

        },
        find_user_event_action: function(event,user_id){
            var return_val = false
            event.members.forEach(member => {
                if (parseInt(member.user.id) == parseInt(user_id)){
                    return_val = member.action
                }
            });
            return return_val
        },
        api_call: function(url,method,json_data="{}"){
            resp = this.async_api_call_axios(url,method,json_data)
            resp.catch(error => {
                this.err_messages.push(error)
            });
            resp.finally(() => {
                this.loading = false;
            });
            return resp
        },
        async_api_call_axios: async(url,method,json_data) =>{
            return await axios({
                url: url,
                method: method,
                data: json_data,
                proxy: '',
                headers: {'Content-Type':'application/json','X-CSRFToken': Cookies.get('csrftoken')}
            });
        }
    }
    
}); 
