MediaAlbum = {};
MediaAlbum.blocks = [];
MediaAlbum.links = [];
MediaAlbum.currentBlock = -1;
MediaAlbum.buttonNext;
MediaAlbum.buttonPrev;

MediaAlbum.getMediaLinks = function ()
{
    jq(".ib-media-album-link").each(function (){
       MediaAlbum.links[MediaAlbum.links.length] = jq(this).attr("href");
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
    if(MediaAlbum.links.length > 0)
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
            .click(function(){MediaAlbum.prev()})
            .css('display','none');
    }
    jq('#ib-media-album').append(prevImg);
    jq('#ib-media-album').append(nextImg);
    MediaAlbum.buttonNext = nextImg;
    MediaAlbum.buttonPrev = prevImg;
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
                jq(block).append(this);
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
        ).attr('src', url+'/image_preview');
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
        if(num === 0)
        {
            jq(MediaAlbum.buttonNext).css('display','none');
            jq(MediaAlbum.buttonPrev).css('display','block');
        }else if(num === MediaAlbum.blocks.length-1)
        {
            jq(MediaAlbum.buttonPrev).css('display','none');
            jq(MediaAlbum.buttonNext).css('display','block');
        }else
        {
            jq(MediaAlbum.buttonNext).css('display','block');
            jq(MediaAlbum.buttonPrev).css('display','block');
        }
    }
}

MediaAlbum.run = function ()
{
    MediaAlbum.getMediaLinks();
    MediaAlbum.loadNextImage();
}

jq(document).ready(function () {MediaAlbum.run();});