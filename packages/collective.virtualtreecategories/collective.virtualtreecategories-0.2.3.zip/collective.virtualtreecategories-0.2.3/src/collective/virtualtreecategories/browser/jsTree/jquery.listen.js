/**
 * jQuery.Listen - Light and fast event handling, using event delegation.
 * Copyright (c) 2007-2008 Ariel Flesler - aflesler(at)gmail(dot)com | http://flesler.blogspot.com
 * Dual licensed under MIT and GPL.
 * Date: 3/7/2008
 * http://flesler.blogspot.com/2007/10/jquerylisten.html
 * @version 1.0.3
 */
;(function($){var a='indexer',h=$.event,j=h.special,k=$.listen=function(c,d,e,f){if(typeof d!='object'){f=e;e=d;d=document}o(c.split(/\s+/),function(a){a=k.fixes[a]||a;var b=m(d,a)||m(d,a,new n(a,d));b.append(e,f);b.start()})},m=function(b,c,d){return $.data(b,c+'.'+a,d)};$.fn[a]=function(a){return this[0]&&m(this[0],a)||null};$[a]=function(a){return m(document,a)};$.extend(k,{regex:/^((?:\w*?|\*))(?:([#.])([\w-]+))?$/,fixes:{focus:'focusin',blur:'focusout'},cache:function(a){this.caching=a}});$.each(k.fixes,function(a,b){j[b]={setup:function(){if($.browser.msie)return!1;this.addEventListener(a,j[b].handler,!0)},teardown:function(){if($.browser.msie)return!1;this.removeEventListener(a,j[b].handler,!0)},handler:function(e){arguments[0]=e=h.fix(e);e.type=b;return h.handle.apply(this,arguments)}}});$.fn.listen=function(a,b,c){return this.each(function(){k(a,this,b,c)})};function n(a,b){$.extend(this,{ids:{},tags:{},listener:b,event:a});this.id=n.instances.push(this)};n.instances=[];n.prototype={constructor:n,handle:function(e){var a=e.stopPropagation;e.stopPropagation=function(){e.stopped=1;a.apply(this,arguments)};m(this,e.type).parse(e);e.stopPropagation=a;a=e.data=null},on:0,bubbles:0,start:function(){var a=this;if(!a.on){h.add(a.listener,a.event,a.handle);a.on=1}},stop:function(){var a=this;if(a.on){h.remove(a.listener,a.event,a.handle);a.on=0}},cache:function(a,b){return $.data(a,'listenCache_'+this.id,b)},parse:function(e){var z=this,c=e.data||e.target,d=arguments,f;if(!k.caching||!(f=z.cache(c))){f=[];if(c.id&&z.ids[c.id])p(f,z.ids[c.id]);o([c.nodeName,'*'],function(a){var b=z.tags[a];if(b)o((c.className+' *').split(' '),function(a){if(a&&b[a])p(f,b[a])})});if(k.caching)z.cache(c,f)}if(f[0]){o(f,function(a){if(a.apply(c,d)===!1){e.preventDefault();e.stopPropagation()}})}if(!e.stopped&&(c=c.parentNode)&&(c.nodeName=='A'||z.bubbles&&c!=z.listener)){e.data=c;z.parse(e)}f=d=c=null},append:function(f,g){var z=this;o(f.split(/\s*,\s*/),function(a){var b=k.regex.exec(a);if(!b)throw'$.listen > "'+a+'" is not a supported selector.';var c=b[2]=='#'&&b[3],d=b[1].toUpperCase()||'*',e=b[3]||'*';if(c)(z.ids[c]||(z.ids[c]=[])).push(g);else if(d){d=z.tags[d]=z.tags[d]||{};(d[e]||(d[e]=[])).push(g)}})}};function o(a,b,c){for(var i=0,l=a.length;i<l;i++)b.call(c,a[i],i)};function p(a,b){a.push.apply(a,b);return a};$(window).unload(function(){if(typeof n=='function')o(n.instances,function(b){b.stop();$.removeData(b.listener,b.event+'.'+a);b.ids=b.names=b.listener=null})})})(jQuery);