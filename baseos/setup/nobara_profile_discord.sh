# this is a hack to disable Discord from trying to update itself. We are only able to receive discord updates from our package repo.
if [ ! -f $HOME/.config/discord/settings.json ];then
    mkdir -p $HOME/.config/discord/
    echo '{' > $HOME/.config/discord/settings.json
    echo '  "SKIP_HOST_UPDATE": true' >> $HOME/.config/discord/settings.json
    echo '}' >> $HOME/.config/discord/settings.json
else
    if [[ -z $(cat $HOME/.config/discord/settings.json | grep SKIP_HOST_UPDATE) ]]; then
        sed -i '2i \  "SKIP_HOST_UPDATE": true,' $HOME/.config/discord/settings.json
    fi
fi
