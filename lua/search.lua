-- Copyright (C) [Mirtle](https://github.com/mirtlecn)
-- License: CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/)
-- 使用说明：<https://github.com/mirtlecn/rime-radical-pinyin/blob/master/search.lua.md>
local function alt_lua_punc( s )
    if s then
        return s:gsub( '([%.%+%-%*%?%[%]%^%$%(%)%%])', '%%%1' )
    else
        return ''
    end
end

local f = {}

function f.init( env )
    local config = env.engine.schema.config
    local ns = 'search'
    f.if_schema_lookup = false
    f.if_reverse_lookup = false

    -- 配置：辅码查字方法
    -- --
    -- 当在 engine 出直接指定了 namespace 则使用该 namespace 进行 schema 匹配
    -- 当在 search_in_cand 节点下指定了 schema 和 db 则进行相应匹配
    -- 当该节点下 schema 为 0 或者 false，或者不存在时，不进行相应匹配
    -- --
    f.schema = config:get_string( ns .. '/schema' )
    if not env.name_space:find( '^%*' ) then f.schema = env.name_space end
    if not f.schema or f.schema == 'false' or f.schema == '0' or #f.schema == 0 then goto checkdb end
    f.mem = Memory( env.engine, Schema( f.schema ) )
    if f.schema and f.mem then
        f.if_schema_lookup = true
        f.schema_search_limit = config:get_int( ns .. '/schema_search_limit' ) or 1000
    end

    ::checkdb::

    local db = config:get_list( ns .. '/db' )
    if db and db.size > 0 then
        f.wildcard = alt_lua_punc( config:get_string( ns .. '/wildcard' ) ) or '*'
        f.db_table = {}
        for i = 0, db.size - 1 do table.insert( f.db_table, ReverseLookup( db:get_value_at( i ).value ) ) end
        f.if_reverse_lookup = true
    end
    if not f.if_reverse_lookup and not f.if_schema_lookup then return end

    -- 配置：辅码转换规则
    -- --
    -- 例如：- xlit/ABCD/1234/ 就可以用 ABCD 来输入 1234（地球拼音音调）
    local fuma_format = config:get_list( ns .. '/fuma_format' )
    if fuma_format and fuma_format.size > 0 then
        f.code_projection = Projection()
        f.code_projection:load( fuma_format )
    end

    -- 配置：是否显示不符合辅码的候选
    f.show_other_cands = config:get_bool( ns .. '/show_other_cands' )
    -- 配置：辅码引导符号，默认为反引号 `
    f.search_key = config:get_string( 'key_binder/search' ) or config:get_string( ns .. '/key' ) or '`'
    f.search_key_string = alt_lua_punc( f.search_key )
    f.code_pattern = config:get_string(ns .. '/code_pattern') or '[a-z]'

    -- 配置：seg tag
    local tag = config:get_list( ns .. '/tags' )
    if tag and tag.size > 0 then
        f.tag = {}
        for i = 0, tag.size - 1 do table.insert( f.tag, tag:get_value_at( i ).value ) end
    else
        f.tag = { 'abc' }
    end

    -- 配置：手动写入用户词库
    local rules = config:get_list( ns .. '/input2code_format' )
    if rules and rules.size > 0 then
        f.projection = Projection()
        f.projection:load( rules )
        f.mem_main = Memory( env.engine, env.engine.schema )
        env.commit_notifier = env.engine.context.commit_notifier:connect(
                                  function( ctx )
                if env.have_select_commit and env.commit_code then
                    local commit_text = ctx:get_commit_text()
                    f.update_dict_entry( commit_text, env.commit_code )
                    ctx.commit_history:push( 'search.lua', commit_text )
                    env.have_select_commit = false
                else
                    return
                end
            end
                               )
    end

    -- 接管选词逻辑，是词组则始终保留引导码，否则直接上屏
    env.notifier = env.engine.context.select_notifier:connect(
                       function( ctx )
            local input = ctx.input
            local code = input:match( '^(.-)' .. f.search_key_string )
            if (not code or #code == 0) then return end

            local preedit = ctx:get_preedit()
            local no_search_string = ctx.input:match( '^(.-)' .. f.search_key_string )
            local edit = preedit.text:match( '^(.-)' .. f.search_key_string )
            env.have_select_commit = true

            if edit and edit:match( f.code_pattern ) then
                ctx.input = no_search_string .. f.search_key
            else
                ctx.input = no_search_string
                env.commit_code = no_search_string
                ctx:commit()
            end
        end
                    )
end

-- try to get the index of special char ·
local function get_pos( text, char )
    local pos = {}
    if text:find( char ) then
        local tmp = text
        for i = 1, utf8.len( tmp ) do
            local first_char = tmp:sub( 1, utf8.offset( tmp, 2 ) - 1 )
            if first_char == char then pos[i] = true end
            tmp = tmp:gsub( '^' .. first_char, '' )
            i = i + 1
        end
    end
    return pos
end

-- 此函数用于手动写入用户词库，目前仅对定长码（如双拼）有效
function f.update_dict_entry( s, code )
    if #s == 0 or utf8.len( s ) == #s or (#code % 2 ~= 0) then
        log.info( '[search.lua]: Ignored' .. s )
        return 0
    end
    local e = DictEntry()
    e.text = s

    local pos = {}
    if s:find( '·' ) and (utf8.len( s ) > 1) then pos = get_pos( s, '·' ) end

    local custom_code = {}
    local loop = 1
    for i = 1, #code, 2 do
        local code_convert = f.projection:apply( code:sub( i, i + 1 ), true )
        if code_convert == 'dian' and pos[loop] then
            -- Ignored
        else
            table.insert( custom_code, code_convert )
        end
        loop = loop + 1
    end

    e.custom_code = table.concat( custom_code, ' ' ) .. ' '
    f.mem_main:update_userdict( e, 1, '' )
end

-- 通过 schema 的方式查询（以辅码查字，然后对比候选，慢，但能够匹配到算法转换过的码）
-- 查询方案中的匹配项，并返回字表
function f.dict_init( search_string )
    local dict_table = {}
    if f.code_projection then search_string = f.code_projection:apply( search_string, true ) end
    if f.mem:dict_lookup( search_string, true, f.schema_search_limit ) then
        for entry in f.mem:iter_dict() do dict_table[entry.text] = true end
    end
    return dict_table
end

-- 匹配候选
function f.dict_match( table, text )
    if table[text] == true then return true end
    return false
end

-- 通过 reverse db 查询（以字查码，然后比对辅码是否相同，快，但只能匹配未经算法转换的码）
function f.reverse_lookup( text, s, global_match )
    s = s:gsub( f.wildcard, '.*' )
    if f.code_projection then s = f.code_projection:apply( s, true ) end
    -- log.error(s)
    for _, db in ipairs( f.db_table ) do
        local code = db:lookup( text )
        for part in code:gmatch( '%S+' ) do
            if global_match then
                if part:find( s ) then return true end
            else
                if part:find( ' ' .. s ) or part:find( '^' .. s ) then return true end
            end
        end
    end
    return false
end

function f.func( input, env )
    -- 当且仅当当输入码中含有辅码引导符号，并有有辅码存在，进入匹配逻辑
    local code, fuma = env.engine.context.input:match( '^(.-)' .. f.search_key_string .. '(.+)$' )
    if (not code or #code == 0) or (not fuma or #fuma == 0) or (not f.if_reverse_lookup and not f.if_schema_lookup) then
        for cand in input:iter() do yield( cand ) end
        return
    end

    local if_single_char_first = env.engine.context:get_option( 'search_single_char' )
    local dict_table
    local fuma_2
    local other_cand = {}
    local long_word_cands = {}
    if f.if_schema_lookup then dict_table = f.dict_init( fuma ) end

    if fuma:find( f.search_key_string ) then fuma, fuma_2 = fuma:match( '^(.-)' .. f.search_key_string .. '(.*)$' ) end

    for cand in input:iter() do
        if cand.type == 'sentence' then goto skip end

        local cand_text = cand.text
        local text = cand_text
        local text_2 = nil

        -- 当候选多于一个字，则取第一个匹配
        if utf8.len( cand_text ) and utf8.len( cand_text ) > 1 then
            text = cand_text:sub( 1, utf8.offset( cand_text, 2 ) - 1 )
            local cand_text_2 = cand_text:gsub( '^' .. text, '' )
            text_2 = cand_text_2:sub( 1, utf8.offset( cand_text_2, 2 ) - 1 )
        end

        if fuma_2 and #fuma_2 > 0 and f.if_reverse_lookup and not f.if_schema_lookup then
            if f.reverse_lookup( text, fuma ) and
                ((text_2 and f.reverse_lookup( text_2, fuma_2 )) or f.reverse_lookup( text, fuma_2, true )) then
                if if_single_char_first and utf8.len( cand.text ) > 1 then
                    table.insert( long_word_cands, cand )
                else
                    yield( cand )
                end
            else
                table.insert( other_cand, cand )
            end
        else
            if (f.if_reverse_lookup and f.reverse_lookup( text, fuma )) or
                (f.if_schema_lookup and f.dict_match( dict_table, text )) then
                if if_single_char_first and utf8.len( cand.text ) > 1 then
                    table.insert( long_word_cands, cand )
                else
                    yield( cand )
                end
            else
                table.insert( other_cand, cand )
            end
        end
        ::skip::
    end

    -- 上屏其余的候选
    for i, cand in ipairs( long_word_cands ) do yield( cand ) end
    if f.show_other_cands then for i, cand in ipairs( other_cand ) do yield( cand ) end end
end

function f.tags_match( seg, env )
    for i, v in ipairs( f.tag ) do if seg.tags[v] then return true end end
    return false
end

function f.fini( env )
    if f.if_reverse_lookup or f.if_schema_lookup then
        env.notifier:disconnect()
        if f.projection then env.commit_notifier:disconnect() end
    end
end

return f
