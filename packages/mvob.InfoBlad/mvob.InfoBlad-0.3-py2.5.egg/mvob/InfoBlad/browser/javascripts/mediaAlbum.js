MediaAlbum = {};
MediaAlbum.blocks = [];
MediaAlbum.links = [];
MediaAlbum.descriptions = [];
MediaAlbum.currentBlock = -1;
MediaAlbum.buttonNext;
MediaAlbum.buttonPrev;

MediaAlbum.getMediaLinks = function ()
{
    jq(".ib-media-album-link").each(function (){
       MediaAlbum.links[MediaAlbum.links.length] = jq(this).attr("href");
       MediaAlbum.descriptions[MediaAlbum.descriptions.length] = jq(this).text()
       MediaAlbum.currentBlock++;
    });
}

MediaAlbum.next = function ()
{
    MediaAlbum.scrollTo(MediaAlbum.currentBlock - 1);
}

MediaAlbum.prev = function ()
{
    MediaAlbum.scrollTo(MediaAlbum.currentBlock + 1);
}

MediaAlbum.addButtons = function ()
{
    if(MediaAlbum.links.length > 1)
    {
        var nextImg = new Image();
        jq(nextImg)
            .addClass("ib-next-button")
            .attr('src', 'buttonNext.jpg')
            .click(function(){MediaAlbum.next()});
        var prevImg = new Image();
        jq(prevImg)
            .addClass("ib-prev-button")
            .attr('src', 'buttonPrev.jpg')
            .click(function(){MediaAlbum.prev()});
            
        jq('#ib-media-album').append(prevImg);
        jq('#ib-media-album').append(nextImg);
        MediaAlbum.buttonNext = nextImg;
        MediaAlbum.buttonPrev = prevImg;
    }
}

MediaAlbum.loadNextImage = function ()
{
    if(MediaAlbum.blocks.length < MediaAlbum.links.length)
    {
        var url = MediaAlbum.links[MediaAlbum.blocks.length];
        var block = jq(document.createElement('div'));
        jq(block).addClass('ib-media-block');
        var img = new Image();
        
        jq(img).load(
            function(){
                // set the image hidden by default    
                jq(this).hide();
                //uncomment to add link to the images
                //link = document.createElement('a');
                //jq(link).attr('href', url);
                //jq(link).append(this);
                //jq(block).append(link);
                jq(block).append(this);
                if(MediaAlbum.descriptions[MediaAlbum.blocks.length] != "")
                {
                    jq(block).append('<div class="ib-media-description">' + MediaAlbum.descriptions[MediaAlbum.blocks.length] + '</div>');
                }
                jq('#ib-media-album-blocks').append(block);
                //fade image in
                jq(this).fadeIn();
                MediaAlbum.blocks[MediaAlbum.blocks.length] = block;
                if (MediaAlbum.blocks.length < MediaAlbum.links.length)
                {
                    MediaAlbum.loadNextImage();
                }else
                {
                    MediaAlbum.addButtons();
                }
            }
        ).attr('src', url+'/image_large');
    }
}

MediaAlbum.scrollTo = function (num)
{
    if(num >= 0 && num < MediaAlbum.blocks.length)
    {
        for(var i=0; i<MediaAlbum.blocks.length; i++)
        {
            if(i === num)
            {
                jq(MediaAlbum.blocks[i]).css('display', 'block');
                MediaAlbum.currentBlock = i;
            }else
            {
                jq(MediaAlbum.blocks[i]).css('display', 'none');
            }
        }
    }
    else if (num === -1)
    {
        MediaAlbum.scrollTo(MediaAlbum.blocks.length-1);
    }
    else if (num === MediaAlbum.blocks.length)
    {
        MediaAlbum.scrollTo(0);
    }
}

MediaAlbum.run = function ()
{
    MediaAlbum.getMediaLinks();
    MediaAlbum.loadNextImage();
}

jq(document).ready(function () {MediaAlbum.run();});