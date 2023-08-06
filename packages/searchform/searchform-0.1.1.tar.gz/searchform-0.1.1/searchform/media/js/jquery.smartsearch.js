/* Search functions for the search form */

(function ($) {

    $.fn.smartsearch = function (request_query_args, options) {

        var settings = $.extend({}, $.fn.smartsearch.defaults, options);

        return this.each(function () {
                var container = this;
                var query = $(".query", container);
                var form = $("form", container);
                var query_args = [];

                // Initialize the searchlet map
                var searchlets = {};
                $(".searchlet", container).each(function () {
                        var css_class = $(this).attr("class");
                        // remove the 'searchlet' part
                        var searchlet_type = css_class.replace("searchlet ", "");
                        var id = $(this).attr("id");
                        var searchlet_name = id.replace("-searchlet", "");
                        var searchlet_function = $.fn.smartsearch.searchlets[searchlet_type];
                        var description = settings.description_map[searchlet_name];
                        var searchlet = new searchlet_function(searchlet_name,
                                                               description,
                                                               settings.update_delay);
                        searchlets[searchlet_name] = searchlet;
                    });

                for (var key in searchlets) {
                    searchlets[key].init();
                }

                /* Some things are hidden by default for accesibility reasons */
                if (settings.use_tabs) {
                    $("#search-sections").show();
                } else {
                    for (var key in searchlets) {
                        searchlets[key].show();
                    }
                }

                /* Display the matching searchlet when clicking on a search section
                   e.g. simulate tabs */
                $(".search-section", container).click(function () {
                        /* show the matching searchlet */
                        if (settings.use_tabs) {
                            $(".searchlet", container).hide();
                            var searchlet = $(this).attr("searchlet");

                            searchlets[searchlet].show();

                            /* highlight the selected section */
                            $(this).parent("li").siblings("li").removeClass("selected");
                            $(this).parent("li").addClass("selected");
                        }
                        return false;
                    });

                /* Function that connect some events to manipulate
 		           a query arg */
                function setup_query_arg() {
                    $(this).click(edit_query_arg)
                         .next("input.remove-action").click(remove_query_arg)
                         .parent("span").hover(function(){$(this).addClass("show-button")},
                                               function(){$(this).removeClass("show-button")});
                }


                /* Function to allow edition on a query arg */
                function edit_query_arg() {
                    var query_arg = $(this).parent("span.query-arg").data("query_arg");
                    // select the searchlet
                    $("a.search-section[searchlet='" + query_arg.attr + "']", container).click();
                    // select the query type
                    searchlets[query_arg.attr].select(query_arg);

                    $("a", query).removeClass("editing");
                    $(this).children("a").addClass("editing");
                    if (settings.debug) dump_query_args("edit_query_arg");
                    return false;
                }

                function remove_query_arg() {
                    var query_arg = $(this).parent("span.query-arg").data("query_arg");
                    for (var i=0; i < query_args.length; i++) {
                        var q = query_args[i];
                        if (q.attr == query_arg.attr && q.operator == query_arg.operator) {
                            remove_query_arg_html(i);
                            searchlets[query_arg.attr].remove(query_arg);
                            query_args.splice(i, 1); // remove the query_arg
                            break;
                        }
                    }
                    if (settings.debug) dump_query_args("remove_query_arg");
                    return false;
                }

                for (var i=0; i < request_query_args.length; i++) {
                    query_args[i] = request_query_args[i];
                    add_query_arg_html(i);
                }

                function add_query_arg_html(query_arg_index) {
                    var attr = query_args[query_arg_index].attr;
                    if(searchlets[attr].show_query_arg){
                        var description = query_args[query_arg_index].description;
                        var value = query_args[query_arg_index].value;
                        var remove_button = '<input type="button" class="remove-action"'
                            + 'value="' + gettext('remove') + '"/>';
                        var rendered_value = searchlets[attr].render_value(value);
                        var contents = '<span class="query-arg">'
                            + (query_arg_index == 0 ? description : gettext('and') + ' ' + description)
                            + ' <a href="#">' + rendered_value + '</a>' + remove_button + '</span>';
                        $(query).append(contents);
                        var query_arg_html = $("span.query-arg:last", query);

                        // double reference the dom node and the query_arg object
                        query_args[query_arg_index].dom = query_arg_html[0];
                        query_arg_html.data("query_arg", query_args[query_arg_index]);

                        query_arg_html.children("a").each(setup_query_arg);
                    }
                }

                function edit_query_arg_html(query_arg_index) {
                    var attr = query_args[query_arg_index].attr;
                    var value = query_args[query_arg_index].value;
                    var rendered_value = searchlets[attr].render_value(value);
                    var query_arg_html = query_args[query_arg_index].dom;
                    $(query_arg_html).children("a").html(rendered_value);
                }

                function remove_query_arg_html(query_arg_index) {
                    var query_arg_html = query_args[query_arg_index].dom;
                    $(query_arg_html).removeData("query_arg");
                    $(query_arg_html).remove();
                    query_args[query_arg_index].dom = null;
                }

                $(".searchlet", container).bind("query_arg_updated", function (event, query_arg) {
                        // find the query_arg
                        var index = -1;
                        for (var i=0; i < query_args.length; i++) {
                            var q = query_args[i];
                            if (q.attr == query_arg.attr && q.operator == query_arg.operator) {
                                q.value = query_arg.value;
                                index = i;
                                if (query_arg.value != "" && query_arg.value != null) {
                                    edit_query_arg_html(i);
                                } else {
                                    remove_query_arg_html(i);
                                    searchlets[query_arg.attr].remove(query_arg);
                                    query_args.splice(i, 1); // remove the query_arg
                                }
                                break;
                            }
                        }
                        if (index == -1) {
                            query_args[query_args.length] = query_arg;
                            if (query_arg.value != "") {
                                add_query_arg_html(query_args.length - 1);
                            }
                        }

                        if (settings.debug) dump_query_args("query_arg_updated handler");

                    });

                // Prepare the data for the GET request
                form.submit(function () {
                        if (settings.debug) dump_query_args("form.submit");

                        for (var i=0; i < query_args.length; i++) {
                            var searchlet = query_args[i].attr;
                            searchlets[searchlet].submit(query_args[i], form);
                        }
                    });

                function dump_query_args(caller) {
                    var msg = $.map(query_args, function (n, i) {
                            return n.attr + " " + n.operator + " " + n.value;
                        });
                    msg = "Current query args (" + caller +"):\n" + msg.join("\n");
                    if (console.debug) {
                        console.debug(msg);
                    } else {
                        alert(msg);
                    }
                };

                /* Select any search term already set */
                $(".query-arg a", container).click();

                /* Make the main area as big as the menu bar */
                menuHeight = $("#search-sections").height();
                searchletHeight = $(".searchlet").height();
                if (searchletHeight < menuHeight) {
                    $(".searchlet").height(menuHeight);
                }

                if (settings.debug) dump_query_args("End main code");

            }); // end of each
    }; // end of smartsearch

    $.fn.smartsearch.defaults = {
        update_delay: 500,
        use_tabs: true,
        descriptions_map: {},
        debug: false
    };

    $.fn.smartsearch.searchlets = {};
    // Base searchlet
    $.fn.smartsearch.searchlets.base = function (searchlet_name, description, update_delay) {
            this.searchlet_name = searchlet_name;
            this.searchlet = $("#" + searchlet_name + '-searchlet');
            this.description = description;
            this.update_delay = update_delay;
    };
    $.fn.smartsearch.searchlets.base.prototype = {
        init: function() {},
        show: function() {
            this.searchlet.show();
        },
        show_query_arg: true,
        render_value: function(value) {},
        select: function(query_arg) {},
        remove: function(query_arg) {},
        submit: function(query_arg, form) {}
    };

    // Text Searchlet
    $.fn.smartsearch.searchlets.text = function (searchlet_name, description, update_delay) {
        $.fn.smartsearch.searchlets.base.call(this, searchlet_name, description, update_delay);
    };
    $.fn.smartsearch.searchlets.text.prototype = new $.fn.smartsearch.searchlets.base;

    $.fn.smartsearch.searchlets.text.prototype.init = function () {
        var searchlet = this.searchlet;
        // When selecting an operator, highlight it
        $(".operators li input", searchlet).click(function () {
                $(".operators li", searchlet).removeClass("selected");
                $(this).parent("li").addClass("selected");
                $(".search-term", searchlet).val("").focus();
            });

        var description = this.description;
        var update_delay = this.update_delay;
        // When typing on the search term update the query
        $(".search-term", searchlet).keyup(function (event) {
                if ($(this).parent().find(".operators li input:checked").size() == 0) {
                    $(this).parent().find(".operators li input:first").attr("checked", "checked");
                }
                var search_term = this;
                var attr = $(this).attr("name");
                setTimeout(function () {
                        var operator_element = $("input[name='" + attr + ".operator']:checked", searchlet);
                        var operator_description = operator_element.next("label").html();

                        var query_arg = {
                            attr: attr,
                            operator: operator_element.val(),
                            value: $(search_term).val(),
                            description: description + ' ' + operator_description,
                            dom: null
                        };

                        searchlet.trigger("query_arg_updated", query_arg);

                    }, update_delay);

            });
    };

    $.fn.smartsearch.searchlets.text.prototype.render_value = function (value) {
        return value;
    };

    $.fn.smartsearch.searchlets.text.prototype.select = function (query_arg) {
        $("input[value='" + query_arg.operator + "']", this.searchlet).change().click();
        $(".search-term", this.searchlet).val(query_arg.value);
    };

    $.fn.smartsearch.searchlets.text.prototype.remove = function (query_arg) {
        $(".search-term", this.searchlet).val("");
        $("input[type=radio]:checked", this.searchlet).removeAttr("checked");
        $(".operators li", this.searchlet).removeClass("selected");
    };

    $.fn.smartsearch.searchlets.text.prototype.submit = function (query_arg, form) {
        var name = query_arg.attr + '__' + query_arg.operator;
        var hidden = "<input type='hidden' name='" + name + "' value='" + query_arg.value + "'/>";
        form.append(hidden);
    };

    // Freetext searchlet
    $.fn.smartsearch.searchlets.freetext = function (searchlet_name, description, update_delay) {
        $.fn.smartsearch.searchlets.text.call(this, searchlet_name, description, update_delay);
    };
    $.fn.smartsearch.searchlets.freetext.prototype = new $.fn.smartsearch.searchlets.text;

    $.fn.smartsearch.searchlets.freetext.prototype.init = function () {
        var searchlet = this.searchlet;
        var attr = this.searchlet_name;
        var description = this.description;
        var update_delay = this.update_delay;
        // When typing on the search term update the query
        $(".search-term", searchlet).keyup(function (event) {
                var search_term = this;
                setTimeout(function () {
                        //var operator_element = $("input[name='" + attr + ".operator']:checked", searchlet);
                        //var operator_description = operator_element.next("label").html();

                        var query_arg = {
                            attr: attr,
                            operator: 'icontains',
                            value: $(search_term).val(),
                            description: description + ' ' + gettext('contains'),
                            dom: null
                        };

                        searchlet.trigger("query_arg_updated", query_arg);

                    }, update_delay);
            });

    };

    $.fn.smartsearch.searchlets.freetext.prototype.select = function (query_arg) {
        $(".search-term", this.searchlet).val(query_arg.value);
    };

    $.fn.smartsearch.searchlets.freetext.prototype.remove = function (query_arg) {
        $(".search-term", this.searchlet).val("");
    };


    // Exclusive options searchlet
    $.fn.smartsearch.searchlets.exclusive_options = function (searchlet_name, description, update_delay) {
        $.fn.smartsearch.searchlets.base.call(this, searchlet_name, description, update_delay);
    };
    $.fn.smartsearch.searchlets.exclusive_options.prototype = new $.fn.smartsearch.searchlets.base;

    // Multiple options searchlet
    $.fn.smartsearch.searchlets.multiple_options = function (searchlet_name, description, update_delay) {
        $.fn.smartsearch.searchlets.base.call(this, searchlet_name, description, update_delay);
    };
    $.fn.smartsearch.searchlets.multiple_options.prototype = new $.fn.smartsearch.searchlets.base;

    $.fn.smartsearch.searchlets.multiple_options.prototype.init = function () {
        var searchlet = this.searchlet;
        $("select", searchlet).easySelect();
        var description = this.description;

        // When the option change update the query
        $("select.search-term", searchlet).bind("options-changed", function () {
                var attr = $(this).attr("name");
                var values = $.map($(this).children("option"), function (option, i) {
                        return $(option).val();
                    });

                var query_arg = {
                    attr: attr,
                    operator: "in",
                    value: values,
                    description: description + ' ' + gettext('is'),
                    dom: null
                };

                searchlet.trigger("query_arg_updated", query_arg);
            });
    };

    $.fn.smartsearch.searchlets.multiple_options.prototype.render_value = function (value) {
        var searchlet = this.searchlet;
        var text_value = $.map(value, function (val, i) {
                return $("option[value=" + val + "]", searchlet).html();
            });
        return text_value.join(", ");
    };

    $.fn.smartsearch.searchlets.multiple_options.prototype.select = function (query_arg) {
        var searchlet = this.searchlet;
        $.each(query_arg.value, function (i, val) {
                $("select:first option[value=" + val + "]", searchlet).attr("selected", "selected");
            });
        move_selected_options($("select:first", searchlet),
                              $("select:last", searchlet));
    };

    $.fn.smartsearch.searchlets.multiple_options.prototype.remove = function (query_arg) {
        $("select:last option", this.searchlet).attr("selected", "selected");
        move_selected_options($("select:last", this.searchlet),
                              $("select:first", this.searchlet));
    };

    $.fn.smartsearch.searchlets.multiple_options.prototype.clean_selects = function (query_arg, form) {
        this.searchlet.find("option:selected").each(function() {
            $(this).attr('selected','');
        });
    };

    $.fn.smartsearch.searchlets.multiple_options.prototype.submit = function (query_arg, form) {
        var name = query_arg.attr + '__' + query_arg.operator;
        for(var i=0; i < query_arg.value.length; i++){
            value = query_arg.value[i];
            var hidden = "<input type='hidden' name='" + name + "' value='" + value + "'/>";
            form.append(hidden);
        }
        this.clean_selects();
    };

    // Hidden searchlet

    $.fn.smartsearch.searchlets.hidden = function (searchlet_name, description, update_delay) {
        $.fn.smartsearch.searchlets.text.call(this, searchlet_name, description, update_delay);
    };
    $.fn.smartsearch.searchlets.hidden.prototype = new $.fn.smartsearch.searchlets.text;

    $.fn.smartsearch.searchlets.hidden.prototype.show_query_arg = false;


    /* Aux private function for the add and delete actions */
    function move_selected_options(src, dst) {
        src.find("option:selected")
            .clone().appendTo(dst)
            .end().remove();
    };

    /* This plugin convert a simple multi select box into a full
       featured double select with buttons to move items around
       between both selects */
    $.fn.easySelect = function () {

        return this.each(function () {
                $(this).removeClass("search-term");
                var name = $(this).attr("name").substring(0, $(this).attr("name").lastIndexOf("__"));
                var size = $(this).attr("size");
                var select_all = "<input type='button' class='select-all-action' value='" + gettext("Select all") + "' />";
                var add_remove = "<div class='add-remove-buttons'>"
                                 + "<input type='button' class='add' value='" + gettext("Add") + "' />"
                                 + "<input type='button' class='delete' value='" + gettext("Remove") + "' />"
                                 + "</div>";
                var selected = "<div class='search-block'>"
                               + "<select class='search-term' multiple='true' "
                               + "size='" + size + "' name='" + name + "' id='" + name +"'>"
                               + "</select>" + select_all + "</div>";
                var searchlet = $(this).parents(".searchlet");
                $(this).after(select_all).parent().after(add_remove + selected);
                $("div", searchlet).wrapAll("<div></div>");

                /* Handy handler for selecting everything on a select */
                $("input.select-all-action", searchlet).click(function() {
                        $(this).prev("select").children("option").attr("selected", "selected");
                        return false;
                    });

                /* Move selected options from the left select to the right */
                $("input.add", searchlet).click(function () {
                        var parent_div = $(this).parent();
                        var src = parent_div.prev().children("select");
                        var dst = parent_div.next().children("select");
                        move_selected_options(src, dst);
                        dst.trigger("options-changed");
                        return false;
                    });

                /* Move selected options from the right select to the left */
                $("input.delete", searchlet).click(function () {
                        var parent_div = $(this).parent();
                        var src = parent_div.prev().children("select");
                        var dst = parent_div.next().children("select");
                        move_selected_options(dst, src);
                        dst.trigger("options-changed");
                        return false;
                    });

            }); // end of each
    }; // end of easySelect

})(jQuery);

