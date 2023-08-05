jQuery(document).ready(function() {
    twttr.anywhere(onAnywhereLoad);
})

function onAnywhereLoad(twitter) {
    var c = ta_config;
    // configure the @Anywhere environment
    if (c.linkify_enabled) {
      twitter.linkifyUsers();      
    } 
    if (c.hovercard_enabled) {
      twitter.hovercards();      
    }
    for (var i=0; i<c.follower_buttons.length; i++) {
      var f = c.follower_buttons[i];
      twitter('#'+f.id).followButton(f.follower);
    }
    for (var i=0; i<c.tweet_boxes.length; i++) {
      var f = c.tweet_boxes[i];
      twitter('#'+f.id).tweetBox(f.conf);
    }
};
