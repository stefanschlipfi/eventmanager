var vueapp = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        events: [],
        err_messages: [],
        _before_edit: new Object(),
        action_btn_dict: new Object(),
        dropdownlabel: "Sort by Action",
    },

    created () {
        this.api_call('http://localhost:8000/api/event/?format=json','GET')
        .then(response => {
            this.init_events(response.data)
        })
        Object.assign(this.action_btn_dict,{'accept':{value: "Zugesagt", class: "success", icon: "done"} })
        Object.assign(this.action_btn_dict,{'maybe':{value: "Mit Vorbehalt", class: "warning", icon: "access_time"} })
        Object.assign(this.action_btn_dict,{'reject':{value: "Abgesagt", class: "danger", icon: "clear"} })

    },
    methods: {
        concat: function(str1,str2){
            return ''.concat(str1,str2)
        },
        init_events: function(event_list){
            this.events = []
            event_list.forEach(item => {
                this.events.push(this.init_event(item));
            });
        },
        init_event: function(event){
            Object.assign(event,{'edit':false});
            Object.assign(event,{'detail':false});
            Object.assign(event,{'card_view':true});
            //set default sorted members to all members
            Object.assign(event,{'sorted_members':event.members});
            return event
        },
        update_event: function(event){
            var new_events_array = []
            this.events.forEach(item => {
                if (parseInt(item.id) == parseInt(event.id))
                    new_events_array.push(event)
                else
                    new_events_array.push(item)
            });
            this.events = new_events_array
        },
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
        sort_members: function(event,action){
            
            this.tab_action_setactive(event,action)
            var sorted_members = []
            if (action == 'all'){
                sorted_members = event.members
                this.dropdownlabel = 'All'
            }else{
                //set dropdown label to action_btn_dict[action].value
                this.dropdownlabel = this.action_btn_dict[action].value
                event.members.forEach(mem => {
                    if (mem.action == action)
                        sorted_members.push(mem)
                });
            }
            var tmpevents = []
            this.events.forEach(item => {
                if (item.id == event.id)
                    Object.assign(item,{'sorted_members':sorted_members});
                tmpevents.push(item);
            });
            this.events = tmpevents
        },
        //workaround for action_modal cannot open modal in js
        get_active_detail_event: function(){
        // find active detail view retrun item / false
            var return_val = false
            this.events.forEach(item => {
                if (item.detail)
                    return_val = item;
            });
            return return_val
        },
        // workaround for disable tab-action active
        tab_action_setactive: function(event,action){
            // disable all
            var actions = ['all','accept','reject','maybe']
            actions.forEach(ac => {
                console.log('#'.concat(event.id,ac))
                var tmp = $('#'.concat(event.id,ac))
                tmp[0].classList.remove('active')
                if (ac == action)
                    tmp[0].classList.add('active')
            });

        },
        submit_action_modal: function(user_id){
            event = this.get_active_detail_event();
            if (event == false){
                this.err_messages.push("cannot find active detail event");
            }else{
                this.err_messages = []
                var action_select = $('#id_action')[0]
                var action = action_select.options[action_select.selectedIndex].value
                var eventuser = this.find_eventuser(event,user_id)
                if (eventuser)  
                    resp = this.update_eventuser(eventuser,action)
                else
                    resp = this.create_eventuser(event,user_id,action)

                resp.then(r => {
                    var event = this.init_event(r.data['event'])
                    event.card_view = false
                    event.detail = true
                    this.update_event(event)
                    this.sort_members(event,action)
                });
            }
        },
        update_eventuser: function(eventuser,action){
            data = new Object
            data['action'] = action
            event = eventuser.event
            return this.api_call(''.concat("http://localhost:8000/api/eventuser/",eventuser.id,"/?format=json"),"PUT",json_data=data)            
        },
        create_eventuser: function(event,user_id,action){
            data = new Object
            data['action'] = action
            data['event_id'] = event.id
            data['user_id'] = user_id
            return this.api_call("http://localhost:8000/api/eventuser/?format=json","POST",json_data=data)
        },

        find_eventuser: function(event,user_id){
            var return_val = false
            event.members.forEach(member => {
                if (parseInt(member.user.id) == parseInt(user_id)){
                    return_val = member
                }
            });
            return return_val
        },
        show_error_message(HTTP_CODE,message){
            error = ''.concat("Code: ",HTTP_CODE,' ',message)
            this.err_messages.push(error)
        },
        api_call: function(url,method,json_data="{}"){
            resp = this.async_api_call_axios(url,method,json_data)
            resp.then(e => {
                this.err_messages = []
            });
            resp.catch(error => {
                this.show_error_message(error.response.status,error.response.data['message'])
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
