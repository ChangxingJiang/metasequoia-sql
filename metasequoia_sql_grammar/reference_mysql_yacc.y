%start start_entry

%%

start_entry:
          sql_statement
        | GRAMMAR_SELECTOR_EXPR bit_expr END_OF_INPUT
          {
            ITEMIZE($2, &$2);
            static_cast<Expression_parser_state *>(YYP)->result= $2;
          }
        | GRAMMAR_SELECTOR_PART partition_clause END_OF_INPUT
          {
            CONTEXTUALIZE($2);
            static_cast<Partition_expr_parser_state *>(YYP)->result=
              &$2->part_info;
          }
        | GRAMMAR_SELECTOR_GCOL IDENT_sys '(' expr ')' END_OF_INPUT
          {
            // Check gcol expression for the "PARSE_GCOL_EXPR" prefix:
            if (!is_identifier($2, "PARSE_GCOL_EXPR"))
              MYSQL_YYABORT;

            auto gcol_info= NEW_PTN Value_generator;
            if (gcol_info == nullptr)
              MYSQL_YYABORT; // OOM
            ITEMIZE($4, &$4);
            gcol_info->expr_item= $4;
            static_cast<Gcol_expr_parser_state *>(YYP)->result= gcol_info;
          }
        | GRAMMAR_SELECTOR_CTE table_subquery END_OF_INPUT
          {
            static_cast<Common_table_expr_parser_state *>(YYP)->result= $2;
          }
        | GRAMMAR_SELECTOR_DERIVED_EXPR expr END_OF_INPUT
         {
           ITEMIZE($2, &$2);
           static_cast<Derived_expr_parser_state *>(YYP)->result= $2;
         }
        ;

simple_statement_or_begin:
          simple_statement      { *parse_tree= $1; }
        | begin_stmt
        ;

simple_statement:
          alter_database_stmt           { $$= nullptr; }
        | alter_event_stmt              { $$= nullptr; }
        | alter_function_stmt           { $$= nullptr; }
        | alter_instance_stmt
        | alter_logfile_stmt            { $$= nullptr; }
        | alter_procedure_stmt          { $$= nullptr; }
        | alter_resource_group_stmt
        | alter_server_stmt             { $$= nullptr; }
        | alter_tablespace_stmt         { $$= nullptr; }
        | alter_undo_tablespace_stmt    { $$= nullptr; }
        | alter_table_stmt
        | alter_user_stmt               { $$= nullptr; }
        | alter_view_stmt               { $$= nullptr; }
        | analyze_table_stmt
        | binlog_base64_event           { $$= nullptr; }
        | call_stmt
        | change                        { $$= nullptr; }
        | check_table_stmt
        | checksum                      { $$= nullptr; }
        | clone_stmt                    { $$= nullptr; }
        | commit                        { $$= nullptr; }
        | create                        { $$= nullptr; }
        | create_index_stmt
        | create_resource_group_stmt
        | create_role_stmt
        | create_srs_stmt
        | create_table_stmt
        | deallocate                    { $$= nullptr; }
        | delete_stmt
        | describe_stmt
        | do_stmt
        | drop_database_stmt            { $$= nullptr; }
        | drop_event_stmt               { $$= nullptr; }
        | drop_function_stmt            { $$= nullptr; }
        | drop_index_stmt
        | drop_logfile_stmt             { $$= nullptr; }
        | drop_procedure_stmt           { $$= nullptr; }
        | drop_resource_group_stmt
        | drop_role_stmt
        | drop_server_stmt              { $$= nullptr; }
        | drop_srs_stmt
        | drop_tablespace_stmt          { $$= nullptr; }
        | drop_undo_tablespace_stmt     { $$= nullptr; }
        | drop_table_stmt               { $$= nullptr; }
        | drop_trigger_stmt             { $$= nullptr; }
        | drop_user_stmt                { $$= nullptr; }
        | drop_view_stmt                { $$= nullptr; }
        | execute                       { $$= nullptr; }
        | explain_stmt
        | flush                         { $$= nullptr; }
        | get_diagnostics               { $$= nullptr; }
        | group_replication             { $$= nullptr; }
        | grant                         { $$= nullptr; }
        | handler_stmt
        | help                          { $$= nullptr; }
        | import_stmt                   { $$= nullptr; }
        | insert_stmt
        | install_stmt
        | kill                          { $$= nullptr; }
        | load_stmt
        | lock                          { $$= nullptr; }
        | optimize_table_stmt
        | keycache_stmt
        | preload_stmt
        | prepare                       { $$= nullptr; }
        | purge                         { $$= nullptr; }
        | release                       { $$= nullptr; }
        | rename                        { $$= nullptr; }
        | repair_table_stmt
        | replace_stmt
        | reset                         { $$= nullptr; }
        | resignal_stmt                 { $$= nullptr; }
        | restart_server_stmt
        | revoke                        { $$= nullptr; }
        | rollback                      { $$= nullptr; }
        | savepoint                     { $$= nullptr; }
        | select_stmt
        | set                           { $$= nullptr; CONTEXTUALIZE($1); }
        | set_resource_group_stmt
        | set_role_stmt
        | show_binary_log_status_stmt
        | show_binary_logs_stmt
        | show_binlog_events_stmt
        | show_character_set_stmt
        | show_collation_stmt
        | show_columns_stmt
        | show_count_errors_stmt
        | show_count_warnings_stmt
        | show_create_database_stmt
        | show_create_event_stmt
        | show_create_function_stmt
        | show_create_procedure_stmt
        | show_create_table_stmt
        | show_create_trigger_stmt
        | show_create_user_stmt
        | show_create_view_stmt
        | show_databases_stmt
        | show_engine_logs_stmt
        | show_engine_mutex_stmt
        | show_engine_status_stmt
        | show_engines_stmt
        | show_errors_stmt
        | show_events_stmt
        | show_function_code_stmt
        | show_function_status_stmt
        | show_grants_stmt
        | show_keys_stmt
        | show_master_status_stmt
        | show_open_tables_stmt
        | show_parse_tree_stmt
        | show_plugins_stmt
        | show_privileges_stmt
        | show_procedure_code_stmt
        | show_procedure_status_stmt
        | show_processlist_stmt
        | show_profile_stmt
        | show_profiles_stmt
        | show_relaylog_events_stmt
        | show_replica_status_stmt
        | show_replicas_stmt
        | show_status_stmt
        | show_table_status_stmt
        | show_tables_stmt
        | show_triggers_stmt
        | show_variables_stmt
        | show_warnings_stmt
        | shutdown_stmt
        | signal_stmt                   { $$= nullptr; }
        | start                         { $$= nullptr; }
        | start_replica_stmt            { $$= nullptr; }
        | stop_replica_stmt             { $$= nullptr; }
        | truncate_stmt
        | uninstall                     { $$= nullptr; }
        | unlock                        { $$= nullptr; }
        | update_stmt
        | use                           { $$= nullptr; }
        | xa                            { $$= nullptr; }
        ;

/* change master */

change_replication_source:
          MASTER_SYM
          {
            push_deprecated_warn(YYTHD, "CHANGE MASTER",
                                        "CHANGE REPLICATION SOURCE");
          }
        | REPLICATION SOURCE_SYM
        ;

change:
          CHANGE change_replication_source TO_SYM
          {
            LEX *lex = Lex;
            lex->sql_command = SQLCOM_CHANGE_MASTER;
            /*
              Clear LEX_MASTER_INFO struct. repl_ignore_server_ids is cleared
              in THD::cleanup_after_query. So it is guaranteed to be empty here.
            */
            assert(Lex->mi.repl_ignore_server_ids.empty());
            lex->mi.set_unspecified();
          }
          source_defs opt_channel
          {
            if (Lex->set_channel_name($6))
              MYSQL_YYABORT;  // OOM
          }
        | CHANGE REPLICATION FILTER_SYM
          {
            THD *thd= YYTHD;
            LEX* lex= thd->lex;
            assert(lex->m_sql_cmd == nullptr);
            lex->sql_command = SQLCOM_CHANGE_REPLICATION_FILTER;
            lex->m_sql_cmd= NEW_PTN Sql_cmd_change_repl_filter();
            if (lex->m_sql_cmd == nullptr)
              MYSQL_YYABORT;
          }
          filter_defs opt_channel
          {
            if (Lex->set_channel_name($6))
              MYSQL_YYABORT;  // OOM
          }
        ;

filter_defs:
          filter_def
        | filter_defs ',' filter_def
        ;
filter_def:
          REPLICATE_DO_DB EQ opt_filter_db_list
          {
            Sql_cmd_change_repl_filter * filter_sql_cmd=
              (Sql_cmd_change_repl_filter*) Lex->m_sql_cmd;
            assert(filter_sql_cmd != nullptr);
            filter_sql_cmd->set_filter_value($3, OPT_REPLICATE_DO_DB);
          }
        | REPLICATE_IGNORE_DB EQ opt_filter_db_list
          {
            Sql_cmd_change_repl_filter * filter_sql_cmd=
              (Sql_cmd_change_repl_filter*) Lex->m_sql_cmd;
            assert(filter_sql_cmd != nullptr);
            filter_sql_cmd->set_filter_value($3, OPT_REPLICATE_IGNORE_DB);
          }
        | REPLICATE_DO_TABLE EQ opt_filter_table_list
          {
            Sql_cmd_change_repl_filter * filter_sql_cmd=
              (Sql_cmd_change_repl_filter*) Lex->m_sql_cmd;
            assert(filter_sql_cmd != nullptr);
            filter_sql_cmd->set_filter_value($3, OPT_REPLICATE_DO_TABLE);
          }
        | REPLICATE_IGNORE_TABLE EQ opt_filter_table_list
          {
            Sql_cmd_change_repl_filter * filter_sql_cmd=
              (Sql_cmd_change_repl_filter*) Lex->m_sql_cmd;
            assert(filter_sql_cmd != nullptr);
            filter_sql_cmd->set_filter_value($3, OPT_REPLICATE_IGNORE_TABLE);
          }
        | REPLICATE_WILD_DO_TABLE EQ opt_filter_string_list
          {
            Sql_cmd_change_repl_filter * filter_sql_cmd=
              (Sql_cmd_change_repl_filter*) Lex->m_sql_cmd;
            assert(filter_sql_cmd != nullptr);
            filter_sql_cmd->set_filter_value($3, OPT_REPLICATE_WILD_DO_TABLE);
          }
        | REPLICATE_WILD_IGNORE_TABLE EQ opt_filter_string_list
          {
            Sql_cmd_change_repl_filter * filter_sql_cmd=
              (Sql_cmd_change_repl_filter*) Lex->m_sql_cmd;
            assert(filter_sql_cmd != nullptr);
            filter_sql_cmd->set_filter_value($3,
                                             OPT_REPLICATE_WILD_IGNORE_TABLE);
          }
        | REPLICATE_REWRITE_DB EQ opt_filter_db_pair_list
          {
            Sql_cmd_change_repl_filter * filter_sql_cmd=
              (Sql_cmd_change_repl_filter*) Lex->m_sql_cmd;
            assert(filter_sql_cmd != nullptr);
            filter_sql_cmd->set_filter_value($3, OPT_REPLICATE_REWRITE_DB);
          }
        ;
opt_filter_db_list:
          '(' ')'
          {
            $$= NEW_PTN mem_root_deque<Item *>(YYMEM_ROOT);
            if ($$ == nullptr)
              MYSQL_YYABORT;
          }
        | '(' filter_db_list ')'
          {
            $$= $2;
          }
        ;

filter_db_list:
          filter_db_ident
          {
            $$= NEW_PTN mem_root_deque<Item *>(YYMEM_ROOT);
            if ($$ == nullptr)
              MYSQL_YYABORT;
            $$->push_back($1);
          }
        | filter_db_list ',' filter_db_ident
          {
            $1->push_back($3);
            $$= $1;
          }
        ;

filter_db_ident:
          ident /* DB name */
          {
            THD *thd= YYTHD;
            Item *db_item= NEW_PTN Item_string($1.str, $1.length,
                                               thd->charset());
            $$= db_item;
          }
        ;
opt_filter_db_pair_list:
          '(' ')'
          {
            $$= NEW_PTN mem_root_deque<Item *>(YYMEM_ROOT);
            if ($$ == nullptr)
              MYSQL_YYABORT;
          }
        |'(' filter_db_pair_list ')'
          {
            $$= $2;
          }
        ;
filter_db_pair_list:
          '(' filter_db_ident ',' filter_db_ident ')'
          {
            $$= NEW_PTN mem_root_deque<Item *>(YYMEM_ROOT);
            if ($$ == nullptr)
              MYSQL_YYABORT;
            $$->push_back($2);
            $$->push_back($4);
          }
        | filter_db_pair_list ',' '(' filter_db_ident ',' filter_db_ident ')'
          {
            $1->push_back($4);
            $1->push_back($6);
            $$= $1;
          }
        ;
opt_filter_table_list:
          '(' ')'
          {
            $$= NEW_PTN mem_root_deque<Item *>(YYMEM_ROOT);
            if ($$ == nullptr)
              MYSQL_YYABORT;
          }
        |'(' filter_table_list ')'
          {
            $$= $2;
          }
        ;

filter_table_list:
          filter_table_ident
          {
            $$= NEW_PTN mem_root_deque<Item *>(YYMEM_ROOT);
            if ($$ == nullptr)
              MYSQL_YYABORT;
            $$->push_back($1);
          }
        | filter_table_list ',' filter_table_ident
          {
            $1->push_back($3);
            $$= $1;
          }
        ;

filter_table_ident:
          schema '.' ident /* qualified table name */
          {
            THD *thd= YYTHD;
            Item_string *table_item= NEW_PTN Item_string($1.str, $1.length,
                                                         thd->charset());
            table_item->append(thd->strmake(".", 1), 1);
            table_item->append($3.str, $3.length);
            $$= table_item;
          }
        ;

opt_filter_string_list:
          '(' ')'
          {
            $$= NEW_PTN mem_root_deque<Item *>(YYMEM_ROOT);
            if ($$ == nullptr)
              MYSQL_YYABORT;
          }
        |'(' filter_string_list ')'
          {
            $$= $2;
          }
        ;

filter_string_list:
          filter_string
          {
            $$= NEW_PTN mem_root_deque<Item *>(YYMEM_ROOT);
            if ($$ == nullptr)
              MYSQL_YYABORT;
            $$->push_back($1);
          }
        | filter_string_list ',' filter_string
          {
            $1->push_back($3);
            $$= $1;
          }
        ;

filter_string:
          filter_wild_db_table_string
          {
            THD *thd= YYTHD;
            Item *string_item= NEW_PTN Item_string($1.str, $1.length,
                                                   thd->charset());
            $$= string_item;
          }
        ;

source_defs:
          source_def
        | source_defs ',' source_def
        ;

change_replication_source_auto_position:
          MASTER_AUTO_POSITION_SYM
          {
            push_deprecated_warn(YYTHD, "MASTER_AUTO_POSITION",
                                        "SOURCE_AUTO_POSITION");

          }
        | SOURCE_AUTO_POSITION_SYM
        ;

change_replication_source_host:
          MASTER_HOST_SYM
          {
            push_deprecated_warn(YYTHD, "MASTER_HOST",
                                        "SOURCE_HOST");
          }
        | SOURCE_HOST_SYM
        ;

change_replication_source_bind:
          MASTER_BIND_SYM
          {
            push_deprecated_warn(YYTHD, "MASTER_BIND",
                                        "SOURCE_BIND");

          }
        | SOURCE_BIND_SYM
        ;

change_replication_source_user:
          MASTER_USER_SYM
          {
            push_deprecated_warn(YYTHD, "MASTER_USER",
                                        "SOURCE_USER");
          }
        | SOURCE_USER_SYM
        ;

change_replication_source_password:
          MASTER_PASSWORD_SYM
          {
            push_deprecated_warn(YYTHD, "MASTER_PASSWORD",
                                        "SOURCE_PASSWORD");
          }
        | SOURCE_PASSWORD_SYM
        ;

change_replication_source_port:
          MASTER_PORT_SYM
          {
            push_deprecated_warn(YYTHD, "MASTER_PORT",
                                        "SOURCE_PORT");
          }
        | SOURCE_PORT_SYM
        ;

change_replication_source_connect_retry:
          MASTER_CONNECT_RETRY_SYM
          {
            push_deprecated_warn(YYTHD, "MASTER_CONNECT_RETRY",
                                        "SOURCE_CONNECT_RETRY");
          }
        | SOURCE_CONNECT_RETRY_SYM
        ;

change_replication_source_retry_count:
          MASTER_RETRY_COUNT_SYM
          {
            push_deprecated_warn(YYTHD, "MASTER_RETRY_COUNT",
                                        "SOURCE_RETRY_COUNT");
          }
        | SOURCE_RETRY_COUNT_SYM
        ;

change_replication_source_delay:
          MASTER_DELAY_SYM
          {
            push_deprecated_warn(YYTHD, "MASTER_DELAY",
                                        "SOURCE_DELAY");
          }
        | SOURCE_DELAY_SYM
        ;

change_replication_source_ssl:
          MASTER_SSL_SYM
          {
            push_deprecated_warn(YYTHD, "MASTER_SSL",
                                        "SOURCE_SSL");
          }
        | SOURCE_SSL_SYM
        ;

change_replication_source_ssl_ca:
          MASTER_SSL_CA_SYM
          {
            push_deprecated_warn(YYTHD, "MASTER_SSL_CA",
                                        "SOURCE_SSL_CA");
          }
        | SOURCE_SSL_CA_SYM
        ;

change_replication_source_ssl_capath:
          MASTER_SSL_CAPATH_SYM
          {
            push_deprecated_warn(YYTHD, "MASTER_SSL_CAPATH",
                                        "SOURCE_SSL_CAPATH");
          }
        | SOURCE_SSL_CAPATH_SYM
        ;

change_replication_source_ssl_cipher:
          MASTER_SSL_CIPHER_SYM
          {
            push_deprecated_warn(YYTHD, "MASTER_SSL_CIPHER",
                                        "SOURCE_SSL_CIPHER");
          }
        | SOURCE_SSL_CIPHER_SYM
        ;

change_replication_source_ssl_crl:
          MASTER_SSL_CRL_SYM
          {
            push_deprecated_warn(YYTHD, "MASTER_SSL_CRL",
                                        "SOURCE_SSL_CRL");
          }
        | SOURCE_SSL_CRL_SYM
        ;

change_replication_source_ssl_crlpath:
          MASTER_SSL_CRLPATH_SYM
          {
            push_deprecated_warn(YYTHD, "MASTER_SSL_CRLPATH",
                                        "SOURCE_SSL_CRLPATH");
          }
        | SOURCE_SSL_CRLPATH_SYM
        ;

change_replication_source_ssl_key:
          MASTER_SSL_KEY_SYM
          {
            push_deprecated_warn(YYTHD, "MASTER_SSL_KEY",
                                        "SOURCE_SSL_KEY");
          }
        | SOURCE_SSL_KEY_SYM
        ;

change_replication_source_ssl_verify_server_cert:
          MASTER_SSL_VERIFY_SERVER_CERT_SYM
          {
            push_deprecated_warn(YYTHD, "MASTER_SSL_VERIFY_SERVER_CERT",
                                        "SOURCE_SSL_VERIFY_SERVER_CERT");
          }
        | SOURCE_SSL_VERIFY_SERVER_CERT_SYM
        ;

change_replication_source_tls_version:
          MASTER_TLS_VERSION_SYM
          {
             push_deprecated_warn(YYTHD, "MASTER_TLS_VERSION",
                                         "SOURCE_TLS_VERSION");
          }
        | SOURCE_TLS_VERSION_SYM
        ;

change_replication_source_tls_ciphersuites:
          MASTER_TLS_CIPHERSUITES_SYM
          {
            push_deprecated_warn(YYTHD, "MASTER_TLS_CIPHERSUITES",
                                        "SOURCE_TLS_CIPHERSUITES");
          }
        | SOURCE_TLS_CIPHERSUITES_SYM
        ;

change_replication_source_ssl_cert:
          MASTER_SSL_CERT_SYM
          {
            push_deprecated_warn(YYTHD, "MASTER_SSL_CERT",
                                        "SOURCE_SSL_CERT");
          }
        | SOURCE_SSL_CERT_SYM
        ;

change_replication_source_public_key:
          MASTER_PUBLIC_KEY_PATH_SYM
          {
            push_deprecated_warn(YYTHD, "MASTER_PUBLIC_KEY_PATH",
                                        "SOURCE_PUBLIC_KEY_PATH");
          }
        | SOURCE_PUBLIC_KEY_PATH_SYM
        ;

change_replication_source_get_source_public_key:
          GET_MASTER_PUBLIC_KEY_SYM
          {
            push_deprecated_warn(YYTHD, "GET_MASTER_PUBLIC_KEY",
                                        "GET_SOURCE_PUBLIC_KEY");
          }
        | GET_SOURCE_PUBLIC_KEY_SYM
        ;

change_replication_source_heartbeat_period:
          MASTER_HEARTBEAT_PERIOD_SYM
          {
            push_deprecated_warn(YYTHD, "MASTER_HEARTBEAT_PERIOD",
                                        "SOURCE_HEARTBEAT_PERIOD");
          }
        | SOURCE_HEARTBEAT_PERIOD_SYM
        ;

change_replication_source_compression_algorithm:
          MASTER_COMPRESSION_ALGORITHM_SYM
          {
            push_deprecated_warn(YYTHD, "MASTER_COMPRESSION_ALGORITHM",
                                        "SOURCE_COMPRESSION_ALGORITHM");
          }
        | SOURCE_COMPRESSION_ALGORITHM_SYM
        ;

change_replication_source_zstd_compression_level:
          MASTER_ZSTD_COMPRESSION_LEVEL_SYM
          {
            push_deprecated_warn(YYTHD, "MASTER_ZSTD_COMPRESSION_LEVEL",
                                        "SOURCE_ZSTD_COMPRESSION_LEVEL");
          }
        | SOURCE_ZSTD_COMPRESSION_LEVEL_SYM
        ;

source_def:
          change_replication_source_host EQ TEXT_STRING_sys_nonewline
          {
            Lex->mi.host = $3.str;
          }
        | NETWORK_NAMESPACE_SYM EQ TEXT_STRING_sys_nonewline
          {
            Lex->mi.network_namespace = $3.str;
          }
        | change_replication_source_bind EQ TEXT_STRING_sys_nonewline
          {
            Lex->mi.bind_addr = $3.str;
          }
        | change_replication_source_user EQ TEXT_STRING_sys_nonewline
          {
            Lex->mi.user = $3.str;
          }
        | change_replication_source_password EQ TEXT_STRING_sys_nonewline
          {
            Lex->mi.password = $3.str;
            if (strlen($3.str) > 32)
            {
              my_error(ER_CHANGE_SOURCE_PASSWORD_LENGTH, MYF(0));
              MYSQL_YYABORT;
            }
            Lex->contains_plaintext_password= true;
          }
        | change_replication_source_port EQ ulong_num
          {
            Lex->mi.port = $3;
          }
        | change_replication_source_connect_retry EQ ulong_num
          {
            Lex->mi.connect_retry = $3;
          }
        | change_replication_source_retry_count EQ ulong_num
          {
            Lex->mi.retry_count= $3;
            Lex->mi.retry_count_opt= LEX_MASTER_INFO::LEX_MI_ENABLE;
          }
        | change_replication_source_delay EQ ulong_num
          {
            if ($3 > MASTER_DELAY_MAX)
            {
              const char *msg= YYTHD->strmake(@3.cpp.start, @3.cpp.end - @3.cpp.start);
              my_error(ER_SOURCE_DELAY_VALUE_OUT_OF_RANGE, MYF(0),
                       msg, MASTER_DELAY_MAX);
            }
            else
              Lex->mi.sql_delay = $3;
          }
        | change_replication_source_ssl EQ ulong_num
          {
            Lex->mi.ssl= $3 ?
              LEX_MASTER_INFO::LEX_MI_ENABLE : LEX_MASTER_INFO::LEX_MI_DISABLE;
          }
        | change_replication_source_ssl_ca EQ TEXT_STRING_sys_nonewline
          {
            Lex->mi.ssl_ca= $3.str;
          }
        | change_replication_source_ssl_capath EQ TEXT_STRING_sys_nonewline
          {
            Lex->mi.ssl_capath= $3.str;
          }
        | change_replication_source_tls_version EQ TEXT_STRING_sys_nonewline
          {
            Lex->mi.tls_version= $3.str;
          }
        | change_replication_source_tls_ciphersuites EQ source_tls_ciphersuites_def
        | change_replication_source_ssl_cert EQ TEXT_STRING_sys_nonewline
          {
            Lex->mi.ssl_cert= $3.str;
          }
        | change_replication_source_ssl_cipher EQ TEXT_STRING_sys_nonewline
          {
            Lex->mi.ssl_cipher= $3.str;
          }
        | change_replication_source_ssl_key EQ TEXT_STRING_sys_nonewline
          {
            Lex->mi.ssl_key= $3.str;
          }
        | change_replication_source_ssl_verify_server_cert EQ ulong_num
          {
            Lex->mi.ssl_verify_server_cert= $3 ?
              LEX_MASTER_INFO::LEX_MI_ENABLE : LEX_MASTER_INFO::LEX_MI_DISABLE;
          }
        | change_replication_source_ssl_crl EQ TEXT_STRING_sys_nonewline
          {
            Lex->mi.ssl_crl= $3.str;
          }
        | change_replication_source_ssl_crlpath EQ TEXT_STRING_sys_nonewline
          {
            Lex->mi.ssl_crlpath= $3.str;
          }
        | change_replication_source_public_key EQ TEXT_STRING_sys_nonewline
          {
            Lex->mi.public_key_path= $3.str;
          }
        | change_replication_source_get_source_public_key EQ ulong_num
          {
            Lex->mi.get_public_key= $3 ?
              LEX_MASTER_INFO::LEX_MI_ENABLE :
              LEX_MASTER_INFO::LEX_MI_DISABLE;
          }
        | change_replication_source_heartbeat_period EQ NUM_literal
          {
            Item *num= $3;
            ITEMIZE(num, &num);

            Lex->mi.heartbeat_period= (float) num->val_real();
            if (Lex->mi.heartbeat_period > SLAVE_MAX_HEARTBEAT_PERIOD ||
                Lex->mi.heartbeat_period < 0.0)
            {
               const char format[]= "%d";
               char buf[4*sizeof(SLAVE_MAX_HEARTBEAT_PERIOD) + sizeof(format)];
               sprintf(buf, format, SLAVE_MAX_HEARTBEAT_PERIOD);
               my_error(ER_REPLICA_HEARTBEAT_VALUE_OUT_OF_RANGE, MYF(0), buf);
               MYSQL_YYABORT;
            }
            if (Lex->mi.heartbeat_period > replica_net_timeout)
            {
              push_warning(YYTHD, Sql_condition::SL_WARNING,
                           ER_REPLICA_HEARTBEAT_VALUE_OUT_OF_RANGE_MAX,
                           ER_THD(YYTHD, ER_REPLICA_HEARTBEAT_VALUE_OUT_OF_RANGE_MAX));
            }
            if (Lex->mi.heartbeat_period < 0.001)
            {
              if (Lex->mi.heartbeat_period != 0.0)
              {
                push_warning(YYTHD, Sql_condition::SL_WARNING,
                             ER_REPLICA_HEARTBEAT_VALUE_OUT_OF_RANGE_MIN,
                             ER_THD(YYTHD, ER_REPLICA_HEARTBEAT_VALUE_OUT_OF_RANGE_MIN));
                Lex->mi.heartbeat_period= 0.0;
              }
              Lex->mi.heartbeat_opt=  LEX_MASTER_INFO::LEX_MI_DISABLE;
            }
            Lex->mi.heartbeat_opt=  LEX_MASTER_INFO::LEX_MI_ENABLE;
          }
        | IGNORE_SERVER_IDS_SYM EQ '(' ignore_server_id_list ')'
          {
            Lex->mi.repl_ignore_server_ids_opt= LEX_MASTER_INFO::LEX_MI_ENABLE;
           }
        | change_replication_source_compression_algorithm EQ TEXT_STRING_sys
          {
            Lex->mi.compression_algorithm = $3.str;
           }
        | change_replication_source_zstd_compression_level EQ ulong_num
          {
            Lex->mi.zstd_compression_level = $3;
           }
        | change_replication_source_auto_position EQ ulong_num
          {
            Lex->mi.auto_position= $3 ?
              LEX_MASTER_INFO::LEX_MI_ENABLE :
              LEX_MASTER_INFO::LEX_MI_DISABLE;
          }
        | PRIVILEGE_CHECKS_USER_SYM EQ privilege_check_def
        | REQUIRE_ROW_FORMAT_SYM EQ ulong_num
          {
            switch($3) {
            case 0:
                Lex->mi.require_row_format =
                  LEX_MASTER_INFO::LEX_MI_DISABLE;
                break;
            case 1:
                Lex->mi.require_row_format =
                  LEX_MASTER_INFO::LEX_MI_ENABLE;
                break;
            default:
              const char* wrong_value = YYTHD->strmake(@3.raw.start, @3.raw.length());
              my_error(ER_REQUIRE_ROW_FORMAT_INVALID_VALUE, MYF(0), wrong_value);
            }
          }
        | REQUIRE_TABLE_PRIMARY_KEY_CHECK_SYM EQ table_primary_key_check_def
        | SOURCE_CONNECTION_AUTO_FAILOVER_SYM EQ real_ulong_num
          {
            switch($3) {
            case 0:
                Lex->mi.m_source_connection_auto_failover =
                  LEX_MASTER_INFO::LEX_MI_DISABLE;
                break;
            case 1:
                Lex->mi.m_source_connection_auto_failover =
                  LEX_MASTER_INFO::LEX_MI_ENABLE;
                break;
            default:
                YYTHD->syntax_error_at(@3);
                MYSQL_YYABORT;
            }
          }
        | ASSIGN_GTIDS_TO_ANONYMOUS_TRANSACTIONS_SYM EQ assign_gtids_to_anonymous_transactions_def
        | GTID_ONLY_SYM EQ real_ulong_num
          {
            switch($3) {
            case 0:
                Lex->mi.m_gtid_only =
                  LEX_MASTER_INFO::LEX_MI_DISABLE;
                break;
            case 1:
                Lex->mi.m_gtid_only =
                  LEX_MASTER_INFO::LEX_MI_ENABLE;
                break;
            default:
                YYTHD->syntax_error_at(@3,
                  "You have an error in your CHANGE REPLICATION SOURCE syntax; GTID_ONLY only accepts values 0 or 1");
                MYSQL_YYABORT;
            }
          }
        | source_file_def
        ;

ignore_server_id_list:
            %empty
          | ignore_server_id
          | ignore_server_id_list ',' ignore_server_id
        ;

ignore_server_id:
          ulong_num
          {
            Lex->mi.repl_ignore_server_ids.push_back($1);
          }

privilege_check_def:
          user_ident_or_text
          {
            Lex->mi.privilege_checks_none= false;
            Lex->mi.privilege_checks_username= $1->user.str;
            Lex->mi.privilege_checks_hostname= $1->host.str;
          }
        | NULL_SYM
          {
            Lex->mi.privilege_checks_none= true;
            Lex->mi.privilege_checks_username= nullptr;
            Lex->mi.privilege_checks_hostname= nullptr;
          }
        ;

table_primary_key_check_def:
          STREAM_SYM
          {
            Lex->mi.require_table_primary_key_check= LEX_MASTER_INFO::LEX_MI_PK_CHECK_STREAM;
          }
        | ON_SYM
          {
            Lex->mi.require_table_primary_key_check= LEX_MASTER_INFO::LEX_MI_PK_CHECK_ON;
          }
        | OFF_SYM
          {
            Lex->mi.require_table_primary_key_check= LEX_MASTER_INFO::LEX_MI_PK_CHECK_OFF;
          }
        | GENERATE_SYM
          {
            Lex->mi.require_table_primary_key_check= LEX_MASTER_INFO::LEX_MI_PK_CHECK_GENERATE;
          }
        ;

assign_gtids_to_anonymous_transactions_def:
          OFF_SYM
          {
            Lex->mi.assign_gtids_to_anonymous_transactions_type = LEX_MASTER_INFO::LEX_MI_ANONYMOUS_TO_GTID_OFF;
          }
        | LOCAL_SYM
          {
            Lex->mi.assign_gtids_to_anonymous_transactions_type = LEX_MASTER_INFO::LEX_MI_ANONYMOUS_TO_GTID_LOCAL;
          }
        | TEXT_STRING
          {
            Lex->mi.assign_gtids_to_anonymous_transactions_type = LEX_MASTER_INFO::LEX_MI_ANONYMOUS_TO_GTID_UUID;
            Lex->mi.assign_gtids_to_anonymous_transactions_manual_uuid = $1.str;
            if (!mysql::gtid::Uuid::is_valid($1.str, mysql::gtid::Uuid::TEXT_LENGTH))
            {
              my_error(ER_WRONG_VALUE, MYF(0), "UUID", $1.str);
              MYSQL_YYABORT;
            }
          }
        ;


source_tls_ciphersuites_def:
          TEXT_STRING_sys_nonewline
          {
            Lex->mi.tls_ciphersuites = LEX_MASTER_INFO::SPECIFIED_STRING;
            Lex->mi.tls_ciphersuites_string= $1.str;
          }
        | NULL_SYM
          {
            Lex->mi.tls_ciphersuites = LEX_MASTER_INFO::SPECIFIED_NULL;
            Lex->mi.tls_ciphersuites_string = nullptr;
          }
        ;

source_log_file:
          MASTER_LOG_FILE_SYM
          {
            push_deprecated_warn(YYTHD, "MASTER_LOG_FILE",
                                        "SOURCE_LOG_FILE");
          }
        | SOURCE_LOG_FILE_SYM
        ;

source_log_pos:
          MASTER_LOG_POS_SYM
          {
            push_deprecated_warn(YYTHD, "MASTER_LOG_POS",
                                        "SOURCE_LOG_POS");
          }
        | SOURCE_LOG_POS_SYM
        ;

source_file_def:
          source_log_file EQ TEXT_STRING_sys_nonewline
          {
            Lex->mi.log_file_name = $3.str;
          }
        | source_log_pos EQ ulonglong_num
          {
            Lex->mi.pos = $3;
            /*
               If the user specified a value < BIN_LOG_HEADER_SIZE, adjust it
               instead of causing subsequent errors.
               We need to do it in this file, because only there we know that
               MASTER_LOG_POS has been explicitely specified. On the contrary
               in change_master() (sql_repl.cc) we cannot distinguish between 0
               (MASTER_LOG_POS explicitely specified as 0) and 0 (unspecified),
               whereas we want to distinguish (specified 0 means "read the binlog
               from 0" (4 in fact), unspecified means "don't change the position
               (keep the preceding value)").
            */
            Lex->mi.pos = max<ulonglong>(BIN_LOG_HEADER_SIZE, Lex->mi.pos);
          }
        | RELAY_LOG_FILE_SYM EQ TEXT_STRING_sys_nonewline
          {
            Lex->mi.relay_log_name = $3.str;
          }
        | RELAY_LOG_POS_SYM EQ ulong_num
          {
            Lex->mi.relay_log_pos = $3;
            /* Adjust if < BIN_LOG_HEADER_SIZE (same comment as Lex->mi.pos) */
            Lex->mi.relay_log_pos = max<ulong>(BIN_LOG_HEADER_SIZE,
                                               Lex->mi.relay_log_pos);
          }
        ;

create:
          CREATE DATABASE opt_if_not_exists ident
          {
            Lex->create_info= YYTHD->alloc_typed<HA_CREATE_INFO>();
            if (Lex->create_info == nullptr)
              MYSQL_YYABORT; // OOM
            Lex->create_info->default_table_charset= nullptr;
            Lex->create_info->used_fields= 0;
          }
          opt_create_database_options
          {
            LEX *lex=Lex;
            lex->sql_command=SQLCOM_CREATE_DB;
            lex->name= $4;
            lex->create_info->options= $3 ? HA_LEX_CREATE_IF_NOT_EXISTS : 0;
          }
        | CREATE view_or_trigger_or_sp_or_event
          {}
        | CREATE USER opt_if_not_exists create_user_list default_role_clause
                      require_clause connect_options
                      opt_account_lock_password_expire_options
                      opt_user_attribute
          {
            LEX *lex=Lex;
            lex->sql_command = SQLCOM_CREATE_USER;
            lex->default_roles= $5;
            Lex->create_info= YYTHD->alloc_typed<HA_CREATE_INFO>();
            if (Lex->create_info == nullptr)
              MYSQL_YYABORT; // OOM
            lex->create_info->options= $3 ? HA_LEX_CREATE_IF_NOT_EXISTS : 0;
            MAKE_CMD_DCL_DUMMY();
          }
        | CREATE LOGFILE_SYM GROUP_SYM ident ADD lg_undofile
          opt_logfile_group_options
          {
            auto pc= NEW_PTN Alter_tablespace_parse_context{YYTHD};
            if (pc == nullptr)
              MYSQL_YYABORT; /* purecov: inspected */ // OOM

            if ($7 != nullptr)
            {
              if (YYTHD->is_error() || contextualize_array(pc, $7))
                MYSQL_YYABORT; /* purecov: inspected */
            }

            Lex->m_sql_cmd= NEW_PTN Sql_cmd_logfile_group{CREATE_LOGFILE_GROUP,
                                                          $4, pc, $6};
            if (!Lex->m_sql_cmd)
              MYSQL_YYABORT; /* purecov: inspected */ //OOM

            Lex->sql_command= SQLCOM_ALTER_TABLESPACE;
          }
        | CREATE TABLESPACE_SYM ident opt_ts_datafile_name
          opt_logfile_group_name opt_tablespace_options
          {
            auto pc= NEW_PTN Alter_tablespace_parse_context{YYTHD};
            if (pc == nullptr)
              MYSQL_YYABORT; /* purecov: inspected */ // OOM

            if ($6 != nullptr)
            {
              if (YYTHD->is_error() || contextualize_array(pc, $6))
                MYSQL_YYABORT;
            }

            auto cmd= NEW_PTN Sql_cmd_create_tablespace{$3, $4, $5, pc};
            if (!cmd)
              MYSQL_YYABORT; /* purecov: inspected */ //OOM
            Lex->m_sql_cmd= cmd;
            Lex->sql_command= SQLCOM_ALTER_TABLESPACE;
          }
        | CREATE UNDO_SYM TABLESPACE_SYM ident ADD ts_datafile
          opt_undo_tablespace_options
          {
            auto pc= NEW_PTN Alter_tablespace_parse_context{YYTHD};
            if (pc == nullptr)
              MYSQL_YYABORT; // OOM

            if ($7 != nullptr)
            {
              if (YYTHD->is_error() || contextualize_array(pc, $7))
                MYSQL_YYABORT;
            }

            auto cmd= NEW_PTN Sql_cmd_create_undo_tablespace{
              CREATE_UNDO_TABLESPACE, $4, $6, pc};
            if (!cmd)
              MYSQL_YYABORT; //OOM
            Lex->m_sql_cmd= cmd;
            Lex->sql_command= SQLCOM_ALTER_TABLESPACE;
          }
        | CREATE SERVER_SYM ident_or_text FOREIGN DATA_SYM WRAPPER_SYM
          ident_or_text OPTIONS_SYM '(' server_options_list ')'
          {
            Lex->sql_command= SQLCOM_CREATE_SERVER;
            if ($3.length == 0)
            {
              my_error(ER_WRONG_VALUE, MYF(0), "server name", "");
              MYSQL_YYABORT;
            }
            Lex->server_options.m_server_name= $3;
            Lex->server_options.set_scheme($7);
            Lex->m_sql_cmd=
              NEW_PTN Sql_cmd_create_server(&Lex->server_options);
          }
        ;

create_srs_stmt:
          CREATE OR_SYM REPLACE_SYM SPATIAL_SYM REFERENCE_SYM SYSTEM_SYM
          real_ulonglong_num srs_attributes
          {
            $$= NEW_PTN PT_create_srs(@$, $7, *$8, true, false);
          }
        | CREATE SPATIAL_SYM REFERENCE_SYM SYSTEM_SYM opt_if_not_exists
          real_ulonglong_num srs_attributes
          {
            $$= NEW_PTN PT_create_srs(@$, $6, *$7, false, $5);
          }
        ;

srs_attributes:
          %empty
          {
            $$ = NEW_PTN Sql_cmd_srs_attributes();
            if (!$$)
              MYSQL_YYABORT_ERROR(ER_DA_OOM, MYF(0)); /* purecov: inspected */
          }
        | srs_attributes NAME_SYM TEXT_STRING_sys_nonewline
          {
            if ($1->srs_name.str != nullptr)
            {
              MYSQL_YYABORT_ERROR(ER_SRS_MULTIPLE_ATTRIBUTE_DEFINITIONS, MYF(0),
                                  "NAME");
            }
            else
            {
              $1->srs_name= $3;
            }
          }
        | srs_attributes DEFINITION_SYM TEXT_STRING_sys_nonewline
          {
            if ($1->definition.str != nullptr)
            {
              MYSQL_YYABORT_ERROR(ER_SRS_MULTIPLE_ATTRIBUTE_DEFINITIONS, MYF(0),
                                  "DEFINITION");
            }
            else
            {
              $1->definition= $3;
            }
          }
        | srs_attributes ORGANIZATION_SYM TEXT_STRING_sys_nonewline
          IDENTIFIED_SYM BY real_ulonglong_num
          {
            if ($1->organization.str != nullptr)
            {
              MYSQL_YYABORT_ERROR(ER_SRS_MULTIPLE_ATTRIBUTE_DEFINITIONS, MYF(0),
                                  "ORGANIZATION");
            }
            else
            {
              $1->organization= $3;
              $1->organization_coordsys_id= $6;
            }
          }
        | srs_attributes DESCRIPTION_SYM TEXT_STRING_sys_nonewline
          {
            if ($1->description.str != nullptr)
            {
              MYSQL_YYABORT_ERROR(ER_SRS_MULTIPLE_ATTRIBUTE_DEFINITIONS, MYF(0),
                                  "DESCRIPTION");
            }
            else
            {
              $1->description= $3;
            }
          }
        ;

default_role_clause:
          %empty
          {
            $$= nullptr;
          }
        |
          DEFAULT_SYM ROLE_SYM role_list
          {
            $$= $3;
          }
        ;

server_options_list:
          server_option
        | server_options_list ',' server_option
        ;

server_option:
          USER TEXT_STRING_sys
          {
            Lex->server_options.set_username($2);
          }
        | HOST_SYM TEXT_STRING_sys
          {
            Lex->server_options.set_host($2);
          }
        | DATABASE TEXT_STRING_sys
          {
            Lex->server_options.set_db($2);
          }
        | OWNER_SYM TEXT_STRING_sys
          {
            Lex->server_options.set_owner($2);
          }
        | PASSWORD TEXT_STRING_sys
          {
            Lex->server_options.set_password($2);
            Lex->contains_plaintext_password= true;
          }
        | SOCKET_SYM TEXT_STRING_sys
          {
            Lex->server_options.set_socket($2);
          }
        | PORT_SYM ulong_num
          {
            Lex->server_options.set_port($2);
          }
        ;

event_tail:
          EVENT_SYM opt_if_not_exists sp_name
          {
            THD *thd= YYTHD;
            LEX *lex=Lex;

            lex->stmt_definition_begin= @1.cpp.start;
            lex->create_info->options= $2 ? HA_LEX_CREATE_IF_NOT_EXISTS : 0;
            if (!(lex->event_parse_data= new (thd->mem_root) Event_parse_data()))
              MYSQL_YYABORT;
            lex->event_parse_data->identifier= $3;
            lex->event_parse_data->on_completion=
                                  Event_parse_data::ON_COMPLETION_DROP;

            lex->sql_command= SQLCOM_CREATE_EVENT;
            /* We need that for disallowing subqueries */
            MAKE_CMD_DDL_DUMMY();
          }
          ON_SYM SCHEDULE_SYM ev_schedule_time
          opt_ev_on_completion
          opt_ev_status
          opt_ev_comment
          DO_SYM ev_sql_stmt
          {
            /*
              sql_command is set here because some rules in ev_sql_stmt
              can overwrite it
            */
            Lex->sql_command= SQLCOM_CREATE_EVENT;
            assert(Lex->m_sql_cmd->sql_cmd_type() == SQL_CMD_DDL);
            assert(Lex->m_sql_cmd->sql_command_code() == SQLCOM_CREATE_EVENT);
          }
        ;

/* Stored FUNCTION parameter declaration list */
sp_fdparam_list:
          %empty
        | sp_fdparams
        ;

sp_fdparams:
          sp_fdparams ',' sp_fdparam
        | sp_fdparam
        ;

sp_fdparam:
          ident type opt_collate
          {
            THD *thd= YYTHD;
            LEX *lex= thd->lex;

            CONTEXTUALIZE($2);
            enum_field_types field_type= $2->type;
            const CHARSET_INFO *cs= $2->get_charset();
            if (merge_sp_var_charset_and_collation(cs, $3, &cs))
              MYSQL_YYABORT;

            sp_pcontext *pctx= lex->get_sp_current_parsing_ctx();

            if (sp_check_name(&$1))
              MYSQL_YYABORT;

            if (pctx->find_variable($1.str, $1.length, true))
            {
              my_error(ER_SP_DUP_PARAM, MYF(0), $1.str);
              MYSQL_YYABORT;
            }

            sp_variable *spvar= pctx->add_variable(thd,
                                                   $1,
                                                   field_type,
                                                   sp_variable::MODE_IN);

            if (spvar->field_def.init(thd, "", field_type,
                                      $2->get_length(), $2->get_dec(),
                                      $2->get_type_flags(),
                                      nullptr, nullptr, &NULL_CSTR, nullptr,
                                      $2->get_interval_list(),
                                      cs ? cs : thd->variables.collation_database,
                                      $3 != nullptr, $2->get_uint_geom_type(),
                                      nullptr, nullptr, {},
                                      dd::Column::enum_hidden_type::HT_VISIBLE))
            {
              MYSQL_YYABORT;
            }

            if (prepare_sp_create_field(thd,
                                        &spvar->field_def))
            {
              MYSQL_YYABORT;
            }
            spvar->field_def.field_name= spvar->name.str;
            spvar->field_def.is_nullable= true;
          }
        ;

/* Stored PROCEDURE parameter declaration list */
sp_pdparam_list:
          %empty
        | sp_pdparams
        ;

sp_pdparams:
          sp_pdparams ',' sp_pdparam
        | sp_pdparam
        ;

sp_pdparam:
          sp_opt_inout ident type opt_collate
          {
            THD *thd= YYTHD;
            LEX *lex= thd->lex;
            sp_pcontext *pctx= lex->get_sp_current_parsing_ctx();

            if (sp_check_name(&$2))
              MYSQL_YYABORT;

            if (pctx->find_variable($2.str, $2.length, true))
            {
              my_error(ER_SP_DUP_PARAM, MYF(0), $2.str);
              MYSQL_YYABORT;
            }

            CONTEXTUALIZE($3);
            enum_field_types field_type= $3->type;
            const CHARSET_INFO *cs= $3->get_charset();
            if (merge_sp_var_charset_and_collation(cs, $4, &cs))
              MYSQL_YYABORT;

            sp_variable *spvar= pctx->add_variable(thd,
                                                   $2,
                                                   field_type,
                                                   (sp_variable::enum_mode) $1);

            if (spvar->field_def.init(thd, "", field_type,
                                      $3->get_length(), $3->get_dec(),
                                      $3->get_type_flags(),
                                      nullptr, nullptr, &NULL_CSTR, nullptr,
                                      $3->get_interval_list(),
                                      cs ? cs : thd->variables.collation_database,
                                      $4 != nullptr, $3->get_uint_geom_type(),
                                      nullptr, nullptr, {},
                                      dd::Column::enum_hidden_type::HT_VISIBLE))
            {
              MYSQL_YYABORT;
            }

            if (prepare_sp_create_field(thd,
                                        &spvar->field_def))
            {
              MYSQL_YYABORT;
            }
            spvar->field_def.field_name= spvar->name.str;
            spvar->field_def.is_nullable= true;
          }
        ;

sp_opt_inout:
          %empty      { $$= sp_variable::MODE_IN; }
        | IN_SYM      { $$= sp_variable::MODE_IN; }
        | OUT_SYM     { $$= sp_variable::MODE_OUT; }
        | INOUT_SYM   { $$= sp_variable::MODE_INOUT; }
        ;

get_diagnostics:
          GET_SYM which_area DIAGNOSTICS_SYM diagnostics_information
          {
            Diagnostics_information *info= $4;

            info->set_which_da($2);

            Lex->keep_diagnostics= DA_KEEP_DIAGNOSTICS; // GET DIAGS doesn't clear them.
            Lex->sql_command= SQLCOM_GET_DIAGNOSTICS;
            Lex->m_sql_cmd= NEW_PTN Sql_cmd_get_diagnostics(info);

            if (Lex->m_sql_cmd == nullptr)
              MYSQL_YYABORT;
          }
        ;

which_area:
        /* If <which area> is not specified, then CURRENT is implicit. */
           %empty { $$= Diagnostics_information::CURRENT_AREA; }
        | CURRENT_SYM
          { $$= Diagnostics_information::CURRENT_AREA; }
        | STACKED_SYM
          { $$= Diagnostics_information::STACKED_AREA; }
        ;

diagnostics_information:
          statement_information
          {
            $$= NEW_PTN Statement_information($1);
            if ($$ == nullptr)
              MYSQL_YYABORT;
          }
        | CONDITION_SYM condition_number condition_information
          {
            $$= NEW_PTN Condition_information($2, $3);
            if ($$ == nullptr)
              MYSQL_YYABORT;
          }
        ;

statement_information:
          statement_information_item
          {
            $$= NEW_PTN List<Statement_information_item>;
            if ($$ == nullptr || $$->push_back($1))
              MYSQL_YYABORT;
          }
        | statement_information ',' statement_information_item
          {
            if ($1->push_back($3))
              MYSQL_YYABORT;
            $$= $1;
          }
        ;

statement_information_item:
          simple_target_specification EQ statement_information_item_name
          {
            $$= NEW_PTN Statement_information_item($3, $1);
            if ($$ == nullptr)
              MYSQL_YYABORT;
          }

simple_target_specification:
          ident
          {
            THD *thd= YYTHD;
            LEX *lex= thd->lex;
            sp_head *sp= lex->sphead;

            /*
              NOTE: lex->sphead is nullptr if we're parsing something like
              'GET DIAGNOSTICS v' outside a stored program. We should throw
              ER_SP_UNDECLARED_VAR in such cases.
            */

            if (!sp)
            {
              my_error(ER_SP_UNDECLARED_VAR, MYF(0), $1.str);
              MYSQL_YYABORT;
            }

            $$=
              create_item_for_sp_var(
                thd, to_lex_cstring($1), nullptr,
                sp->m_parser_data.get_current_stmt_start_ptr(),
                @1.raw.start,
                @1.raw.end);

            if ($$ == nullptr)
              MYSQL_YYABORT;
          }
        | '@' ident_or_text
          {
            $$= NEW_PTN Item_func_get_user_var(@$, $2);
            ITEMIZE($$, &$$);
          }
        ;

statement_information_item_name:
          NUMBER_SYM
          { $$= Statement_information_item::NUMBER; }
        | ROW_COUNT_SYM
          { $$= Statement_information_item::ROW_COUNT; }
        ;

condition_information:
          condition_information_item
          {
            $$= NEW_PTN List<Condition_information_item>;
            if ($$ == nullptr || $$->push_back($1))
              MYSQL_YYABORT;
          }
        | condition_information ',' condition_information_item
          {
            if ($1->push_back($3))
              MYSQL_YYABORT;
            $$= $1;
          }
        ;

condition_information_item:
          simple_target_specification EQ condition_information_item_name
          {
            $$= NEW_PTN Condition_information_item($3, $1);
            if ($$ == nullptr)
              MYSQL_YYABORT;
          }

condition_information_item_name:
          CLASS_ORIGIN_SYM
          { $$= Condition_information_item::CLASS_ORIGIN; }
        | SUBCLASS_ORIGIN_SYM
          { $$= Condition_information_item::SUBCLASS_ORIGIN; }
        | CONSTRAINT_CATALOG_SYM
          { $$= Condition_information_item::CONSTRAINT_CATALOG; }
        | CONSTRAINT_SCHEMA_SYM
          { $$= Condition_information_item::CONSTRAINT_SCHEMA; }
        | CONSTRAINT_NAME_SYM
          { $$= Condition_information_item::CONSTRAINT_NAME; }
        | CATALOG_NAME_SYM
          { $$= Condition_information_item::CATALOG_NAME; }
        | SCHEMA_NAME_SYM
          { $$= Condition_information_item::SCHEMA_NAME; }
        | TABLE_NAME_SYM
          { $$= Condition_information_item::TABLE_NAME; }
        | COLUMN_NAME_SYM
          { $$= Condition_information_item::COLUMN_NAME; }
        | CURSOR_NAME_SYM
          { $$= Condition_information_item::CURSOR_NAME; }
        | MESSAGE_TEXT_SYM
          { $$= Condition_information_item::MESSAGE_TEXT; }
        | MYSQL_ERRNO_SYM
          { $$= Condition_information_item::MYSQL_ERRNO; }
        | RETURNED_SQLSTATE_SYM
          { $$= Condition_information_item::RETURNED_SQLSTATE; }
        ;

trg_action_time:
            BEFORE_SYM
            { $$= TRG_ACTION_BEFORE; }
          | AFTER_SYM
            { $$= TRG_ACTION_AFTER; }
          ;

trg_event:
            INSERT_SYM
            { $$= TRG_EVENT_INSERT; }
          | UPDATE_SYM
            { $$= TRG_EVENT_UPDATE; }
          | DELETE_SYM
            { $$= TRG_EVENT_DELETE; }
          ;
/*
  This part of the parser contains common code for all TABLESPACE
  commands.
  CREATE TABLESPACE_SYM name ...
  ALTER TABLESPACE_SYM name ADD DATAFILE ...
  CREATE LOGFILE GROUP_SYM name ...
  ALTER LOGFILE GROUP_SYM name ADD UNDOFILE ..
  DROP TABLESPACE_SYM name
  DROP LOGFILE GROUP_SYM name
*/

opt_ts_datafile_name:
      %empty { $$= { nullptr, 0}; }
    | ADD ts_datafile
      {
        $$ = $2;
      }
    ;

opt_logfile_group_name:
          %empty { $$= { nullptr, 0}; }
        | USE_SYM LOGFILE_SYM GROUP_SYM ident
          {
            $$= $4;
          }
        ;

opt_tablespace_options:
          %empty { $$= nullptr; }
        | tablespace_option_list
        ;

tablespace_option_list:
          tablespace_option
          {
            $$= NEW_PTN Mem_root_array<PT_alter_tablespace_option_base*>(YYMEM_ROOT);
            if ($$ == nullptr || $$->push_back($1))
              MYSQL_YYABORT; /* purecov: inspected */ // OOM
          }
        | tablespace_option_list opt_comma tablespace_option
          {
            $$= $1;
            if ($$->push_back($3))
              MYSQL_YYABORT; /* purecov: inspected */ // OOM
          }
        ;

tablespace_option:
          ts_option_initial_size
        | ts_option_autoextend_size
        | ts_option_max_size
        | ts_option_extent_size
        | ts_option_nodegroup
        | ts_option_engine
        | ts_option_wait
        | ts_option_comment
        | ts_option_file_block_size
        | ts_option_encryption
        | ts_option_engine_attribute
        ;

opt_alter_tablespace_options:
          %empty { $$= nullptr; }
        | alter_tablespace_option_list
        ;

alter_tablespace_option_list:
          alter_tablespace_option
          {
            $$= NEW_PTN Mem_root_array<PT_alter_tablespace_option_base*>(YYMEM_ROOT);
            if ($$ == nullptr || $$->push_back($1))
              MYSQL_YYABORT; /* purecov: inspected */ // OOM
          }
        | alter_tablespace_option_list opt_comma alter_tablespace_option
          {
            $$= $1;
            if ($$->push_back($3))
              MYSQL_YYABORT; /* purecov: inspected */ // OOM
          }
        ;

alter_tablespace_option:
          ts_option_initial_size
        | ts_option_autoextend_size
        | ts_option_max_size
        | ts_option_engine
        | ts_option_wait
        | ts_option_encryption
        | ts_option_engine_attribute
        ;

opt_logfile_group_options:
          %empty { $$= nullptr; }
        | logfile_group_option_list
        ;

logfile_group_option_list:
          logfile_group_option
          {
            $$= NEW_PTN Mem_root_array<PT_alter_tablespace_option_base*>(YYMEM_ROOT);
            if ($$ == nullptr || $$->push_back($1))
              MYSQL_YYABORT; /* purecov: inspected */ // OOM
          }
        | logfile_group_option_list opt_comma logfile_group_option
          {
            $$= $1;
            if ($$->push_back($3))
              MYSQL_YYABORT; /* purecov: inspected */ // OOM
          }
        ;

logfile_group_option:
          ts_option_initial_size
        | ts_option_undo_buffer_size
        | ts_option_redo_buffer_size
        | ts_option_nodegroup
        | ts_option_engine
        | ts_option_wait
        | ts_option_comment
        ;

opt_alter_logfile_group_options:
          %empty { $$= nullptr; }
        | alter_logfile_group_option_list
        ;

alter_logfile_group_option_list:
          alter_logfile_group_option
          {
            $$= NEW_PTN Mem_root_array<PT_alter_tablespace_option_base*>(YYMEM_ROOT);
            if ($$ == nullptr || $$->push_back($1))
              MYSQL_YYABORT; /* purecov: inspected */ // OOM
          }
        | alter_logfile_group_option_list opt_comma alter_logfile_group_option
          {
            $$= $1;
            if ($$->push_back($3))
              MYSQL_YYABORT; /* purecov: inspected */ // OOM
          }
        ;

alter_logfile_group_option:
          ts_option_initial_size
        | ts_option_engine
        | ts_option_wait
        ;

ts_datafile:
          DATAFILE_SYM TEXT_STRING_sys { $$= $2; }
        ;

undo_tablespace_state:
          ACTIVE_SYM   { $$= ALTER_UNDO_TABLESPACE_SET_ACTIVE; }
        | INACTIVE_SYM { $$= ALTER_UNDO_TABLESPACE_SET_INACTIVE; }
        ;

lg_undofile:
          UNDOFILE_SYM TEXT_STRING_sys { $$= $2; }
        ;

ts_option_initial_size:
          INITIAL_SIZE_SYM opt_equal size_number
          {
            $$= NEW_PTN PT_alter_tablespace_option_initial_size(@$, $3);
          }
        ;

ts_option_max_size:
          MAX_SIZE_SYM opt_equal size_number
          {
            $$= NEW_PTN PT_alter_tablespace_option_max_size(@$, $3);
          }
        ;

ts_option_extent_size:
          EXTENT_SIZE_SYM opt_equal size_number
          {
            $$= NEW_PTN PT_alter_tablespace_option_extent_size(@$, $3);
          }
        ;

ts_option_undo_buffer_size:
          UNDO_BUFFER_SIZE_SYM opt_equal size_number
          {
            $$= NEW_PTN PT_alter_tablespace_option_undo_buffer_size(@$, $3);
          }
        ;

ts_option_redo_buffer_size:
          REDO_BUFFER_SIZE_SYM opt_equal size_number
          {
            $$= NEW_PTN PT_alter_tablespace_option_redo_buffer_size(@$, $3);
          }
        ;

ts_option_nodegroup:
          NODEGROUP_SYM opt_equal real_ulong_num
          {
            $$= NEW_PTN PT_alter_tablespace_option_nodegroup(@$, $3);
          }
        ;

ts_option_comment:
          COMMENT_SYM opt_equal TEXT_STRING_sys
          {
            $$= NEW_PTN PT_alter_tablespace_option_comment(@$, $3);
          }
        ;

ts_option_file_block_size:
          FILE_BLOCK_SIZE_SYM opt_equal size_number
          {
            $$= NEW_PTN PT_alter_tablespace_option_file_block_size(@$, $3);
          }
        ;

ts_option_encryption:
          ENCRYPTION_SYM opt_equal TEXT_STRING_sys
          {
            $$= NEW_PTN PT_alter_tablespace_option_encryption(@$, $3);
          }
        ;

ts_option_engine_attribute:
          ENGINE_ATTRIBUTE_SYM opt_equal json_attribute
          {
            $$ = make_tablespace_engine_attribute(YYMEM_ROOT, $3);
          }
        ;

/*
  End tablespace part
*/

udf_type:
          STRING_SYM {$$ = (int) STRING_RESULT; }
        | REAL_SYM {$$ = (int) REAL_RESULT; }
        | DECIMAL_SYM {$$ = (int) DECIMAL_RESULT; }
        | INT_SYM {$$ = (int) INT_RESULT; }
        ;

old_or_new_charset_name_or_default:
          old_or_new_charset_name { $$=$1;   }
        | DEFAULT_SYM    { $$=nullptr; }
        ;

visibility:
          VISIBLE_SYM { $$= true; }
        | INVISIBLE_SYM { $$= false; }
        ;

/*
** Alter table
*/

alter_table_stmt:
          ALTER TABLE_SYM table_ident opt_alter_table_actions
          {
            $$= NEW_PTN PT_alter_table_stmt(
                  @$,
                  YYMEM_ROOT,
                  $3,
                  $4.actions,
                  $4.flags.algo.get_or_default(),
                  $4.flags.lock.get_or_default(),
                  $4.flags.validation.get_or_default());
          }
        | ALTER TABLE_SYM table_ident standalone_alter_table_action
          {
            $$= NEW_PTN PT_alter_table_standalone_stmt(
                  @$,
                  YYMEM_ROOT,
                  $3,
                  $4.action,
                  $4.flags.algo.get_or_default(),
                  $4.flags.lock.get_or_default(),
                  $4.flags.validation.get_or_default());
          }
        ;

alter_view_stmt:
          ALTER view_algorithm definer_opt
          {
            LEX *lex= Lex;

            if (lex->sphead)
            {
              my_error(ER_SP_BADSTATEMENT, MYF(0), "ALTER VIEW");
              MYSQL_YYABORT;
            }
            lex->create_view_mode= enum_view_create_mode::VIEW_ALTER;
          }
          view_tail
          {
            MAKE_CMD_DDL_DUMMY();
          }
        | ALTER definer_opt
          /*
            We have two separate rules for ALTER VIEW rather that
            optional view_algorithm above, to resolve the ambiguity
            with the ALTER EVENT below.
          */
          {
            LEX *lex= Lex;

            if (lex->sphead)
            {
              my_error(ER_SP_BADSTATEMENT, MYF(0), "ALTER VIEW");
              MYSQL_YYABORT;
            }
            lex->create_view_algorithm= VIEW_ALGORITHM_UNDEFINED;
            lex->create_view_mode= enum_view_create_mode::VIEW_ALTER;
          }
          view_tail
          {
            MAKE_CMD_DDL_DUMMY();
          }
        ;

alter_event_stmt:
          ALTER definer_opt EVENT_SYM sp_name
          {
            /*
              It is safe to use Lex->spname because
              ALTER EVENT xxx RENATE TO yyy DO ALTER EVENT RENAME TO
              is not allowed. Lex->spname is used in the case of RENAME TO
              If it had to be supported spname had to be added to
              Event_parse_data.
            */

            if (!(Lex->event_parse_data= new (YYTHD->mem_root) Event_parse_data()))
              MYSQL_YYABORT;
            Lex->event_parse_data->identifier= $4;

            Lex->sql_command= SQLCOM_ALTER_EVENT;
            MAKE_CMD_DDL_DUMMY();
          }
          ev_alter_on_schedule_completion
          opt_ev_rename_to
          opt_ev_status
          opt_ev_comment
          opt_ev_sql_stmt
          {
            if (!($6 || $7 || $8 || $9 || $10))
            {
              YYTHD->syntax_error();
              MYSQL_YYABORT;
            }
            /*
              sql_command is set here because some rules in ev_sql_stmt
              can overwrite it
            */
            Lex->sql_command= SQLCOM_ALTER_EVENT;

            /*
              assert that even if sql_command was overwritten,
              m_sql_cmd was not changed to a different command-type.
            */
            assert(Lex->m_sql_cmd->sql_cmd_type() == SQL_CMD_DDL);
            assert(Lex->m_sql_cmd->sql_command_code() == SQLCOM_ALTER_EVENT);
          }
        ;

alter_logfile_stmt:
          ALTER LOGFILE_SYM GROUP_SYM ident ADD lg_undofile
          opt_alter_logfile_group_options
          {
            auto pc= NEW_PTN Alter_tablespace_parse_context{YYTHD};
            if (pc == nullptr)
              MYSQL_YYABORT; /* purecov: inspected */ // OOM

            if ($7 != nullptr)
            {
              if (YYTHD->is_error() || contextualize_array(pc, $7))
                MYSQL_YYABORT; /* purecov: inspected */
            }

            Lex->m_sql_cmd= NEW_PTN Sql_cmd_logfile_group{ALTER_LOGFILE_GROUP,
                                                          $4, pc, $6};
            if (!Lex->m_sql_cmd)
              MYSQL_YYABORT; /* purecov: inspected */ //OOM

            Lex->sql_command= SQLCOM_ALTER_TABLESPACE;
          }

alter_tablespace_stmt:
          ALTER TABLESPACE_SYM ident ADD ts_datafile
          opt_alter_tablespace_options
          {
            auto pc= NEW_PTN Alter_tablespace_parse_context{YYTHD};
            if (pc == nullptr)
              MYSQL_YYABORT; /* purecov: inspected */ // OOM

            if ($6 != nullptr)
            {
              if (YYTHD->is_error() || contextualize_array(pc, $6))
                MYSQL_YYABORT; /* purecov: inspected */
            }

            Lex->m_sql_cmd= NEW_PTN Sql_cmd_alter_tablespace_add_datafile{$3, $5, pc};
            if (!Lex->m_sql_cmd)
              MYSQL_YYABORT; /* purecov: inspected */ // OOM

            Lex->sql_command= SQLCOM_ALTER_TABLESPACE;
          }
        | ALTER TABLESPACE_SYM ident DROP ts_datafile
          opt_alter_tablespace_options
          {
            auto pc= NEW_PTN Alter_tablespace_parse_context{YYTHD};
            if (pc == nullptr)
              MYSQL_YYABORT; /* purecov: inspected */ // OOM

            if ($6 != nullptr)
            {
              if (YYTHD->is_error() || contextualize_array(pc, $6))
                MYSQL_YYABORT; /* purecov: inspected */
            }

            Lex->m_sql_cmd=
              NEW_PTN Sql_cmd_alter_tablespace_drop_datafile{$3, $5, pc};
            if (!Lex->m_sql_cmd)
              MYSQL_YYABORT; /* purecov: inspected */ // OOM

            Lex->sql_command= SQLCOM_ALTER_TABLESPACE;
          }
        | ALTER TABLESPACE_SYM ident RENAME TO_SYM ident
          {
            Lex->m_sql_cmd= NEW_PTN Sql_cmd_alter_tablespace_rename{$3, $6};
            if (!Lex->m_sql_cmd)
              MYSQL_YYABORT; // OOM

            Lex->sql_command= SQLCOM_ALTER_TABLESPACE;
          }
        | ALTER TABLESPACE_SYM ident alter_tablespace_option_list
          {
            auto pc= NEW_PTN Alter_tablespace_parse_context{YYTHD};
            if (pc == nullptr)
              MYSQL_YYABORT; // OOM

            if ($4 != nullptr)
            {
              if (YYTHD->is_error() || contextualize_array(pc, $4))
                MYSQL_YYABORT;
            }

            Lex->m_sql_cmd=
              NEW_PTN Sql_cmd_alter_tablespace{$3, pc};
            if (!Lex->m_sql_cmd)
              MYSQL_YYABORT; // OOM

            Lex->sql_command= SQLCOM_ALTER_TABLESPACE;
          }
        ;

alter_undo_tablespace_stmt:
          ALTER UNDO_SYM TABLESPACE_SYM ident SET_SYM undo_tablespace_state
          opt_undo_tablespace_options
          {
            auto pc= NEW_PTN Alter_tablespace_parse_context{YYTHD};
            if (pc == nullptr)
              MYSQL_YYABORT; // OOM

            if ($7 != nullptr)
            {
              if (YYTHD->is_error() || contextualize_array(pc, $7))
                MYSQL_YYABORT;
            }

            auto cmd= NEW_PTN Sql_cmd_alter_undo_tablespace{
              ALTER_UNDO_TABLESPACE, $4,
              {nullptr, 0}, pc, $6};
            if (!cmd)
              MYSQL_YYABORT; //OOM
            Lex->m_sql_cmd= cmd;
            Lex->sql_command= SQLCOM_ALTER_TABLESPACE;
          }
        ;

alter_server_stmt:
          ALTER SERVER_SYM ident_or_text OPTIONS_SYM '(' server_options_list ')'
          {
            LEX *lex= Lex;
            lex->sql_command= SQLCOM_ALTER_SERVER;
            lex->server_options.m_server_name= $3;
            lex->m_sql_cmd=
              NEW_PTN Sql_cmd_alter_server(&Lex->server_options);
          }
        ;

alter_user_stmt:
          alter_user_command alter_user_list require_clause
          connect_options opt_account_lock_password_expire_options
          opt_user_attribute
        | alter_user_command user_func identified_by_random_password
          opt_replace_password opt_retain_current_password
          {
            $2->first_factor_auth_info = *$3;

            if ($4.str != nullptr) {
              $2->current_auth = $4;
              $2->uses_replace_clause = true;
            }
            $2->discard_old_password = false;
            $2->retain_current_password = $5;
          }
        | alter_user_command user_func identified_by_password
          opt_replace_password opt_retain_current_password
          {
            $2->first_factor_auth_info = *$3;

            if ($4.str != nullptr) {
              $2->current_auth = $4;
              $2->uses_replace_clause = true;
            }
            $2->discard_old_password = false;
            $2->retain_current_password = $5;
          }
        | alter_user_command user_func DISCARD_SYM OLD_SYM PASSWORD
          {
            $2->discard_old_password = true;
            $2->retain_current_password = false;
          }
        | alter_user_command user DEFAULT_SYM ROLE_SYM ALL
          {
            List<LEX_USER> *users= new (YYMEM_ROOT) List<LEX_USER>;
            if (users == nullptr || users->push_back($2))
              MYSQL_YYABORT;
            List<LEX_USER> *role_list= new (YYMEM_ROOT) List<LEX_USER>;
            auto *tmp=
                NEW_PTN PT_alter_user_default_role(@$, Lex->drop_if_exists,
                                                   users, role_list,
                                                   role_enum::ROLE_ALL);
              MAKE_CMD(tmp);
          }
        | alter_user_command user DEFAULT_SYM ROLE_SYM NONE_SYM
          {
            List<LEX_USER> *users= new (YYMEM_ROOT) List<LEX_USER>;
            if (users == nullptr || users->push_back($2))
              MYSQL_YYABORT;
            List<LEX_USER> *role_list= new (YYMEM_ROOT) List<LEX_USER>;
            auto *tmp=
                NEW_PTN PT_alter_user_default_role(@$, Lex->drop_if_exists,
                                                   users, role_list,
                                                   role_enum::ROLE_NONE);
              MAKE_CMD(tmp);
          }
        | alter_user_command user DEFAULT_SYM ROLE_SYM role_list
          {
            List<LEX_USER> *users= new (YYMEM_ROOT) List<LEX_USER>;
            if (users == nullptr || users->push_back($2))
              MYSQL_YYABORT;
            auto *tmp=
              NEW_PTN PT_alter_user_default_role(@$, Lex->drop_if_exists,
                                                 users, $5,
                                                 role_enum::ROLE_NAME);
            MAKE_CMD(tmp);
          }
        | alter_user_command user opt_user_registration
          {
            if ($2->mfa_list.push_back($3))
              MYSQL_YYABORT;  // OOM
            LEX *lex=Lex;
            lex->users_list.push_front ($2);
          }
        | alter_user_command user_func opt_user_registration
          {
            if ($2->mfa_list.push_back($3))
              MYSQL_YYABORT;  // OOM
          }
        ;

opt_replace_password:
          %empty { $$ = LEX_CSTRING{nullptr, 0}; }
        | REPLACE_SYM TEXT_STRING_password  { $$ = to_lex_cstring($2); }
        ;

alter_user_command:
          ALTER USER if_exists
          {
            LEX *lex= Lex;
            lex->sql_command= SQLCOM_ALTER_USER;
            lex->drop_if_exists= $3;
            MAKE_CMD_DCL_DUMMY();
          }
        ;

opt_user_attribute:
          %empty
          {
            LEX *lex= Lex;
            lex->alter_user_attribute =
              enum_alter_user_attribute::ALTER_USER_COMMENT_NOT_USED;
          }
        | ATTRIBUTE_SYM TEXT_STRING_literal
          {
            LEX *lex= Lex;
            lex->alter_user_attribute =
              enum_alter_user_attribute::ALTER_USER_ATTRIBUTE;
            lex->alter_user_comment_text = $2;
          }
        | COMMENT_SYM TEXT_STRING_literal
          {
            LEX *lex= Lex;
            lex->alter_user_attribute =
              enum_alter_user_attribute::ALTER_USER_COMMENT;
            lex->alter_user_comment_text = $2;
          }
        ;
opt_account_lock_password_expire_options:
          %empty {}
        | opt_account_lock_password_expire_option_list
        ;

opt_account_lock_password_expire_option_list:
          opt_account_lock_password_expire_option
        | opt_account_lock_password_expire_option_list opt_account_lock_password_expire_option
        ;

opt_account_lock_password_expire_option:
          ACCOUNT_SYM UNLOCK_SYM
          {
            LEX *lex=Lex;
            lex->alter_password.update_account_locked_column= true;
            lex->alter_password.account_locked= false;
          }
        | ACCOUNT_SYM LOCK_SYM
          {
            LEX *lex=Lex;
            lex->alter_password.update_account_locked_column= true;
            lex->alter_password.account_locked= true;
          }
        | PASSWORD EXPIRE_SYM
          {
            LEX *lex= Lex;
            lex->alter_password.expire_after_days= 0;
            lex->alter_password.update_password_expired_column= true;
            lex->alter_password.update_password_expired_fields= true;
            lex->alter_password.use_default_password_lifetime= true;
          }
        | PASSWORD EXPIRE_SYM INTERVAL_SYM real_ulong_num DAY_SYM
          {
            LEX *lex= Lex;
            if ($4 == 0 || $4 > UINT_MAX16)
            {
              char buf[MAX_BIGINT_WIDTH + 1];
              snprintf(buf, sizeof(buf), "%lu", $4);
              my_error(ER_WRONG_VALUE, MYF(0), "DAY", buf);
              MYSQL_YYABORT;
            }
            lex->alter_password.expire_after_days= $4;
            lex->alter_password.update_password_expired_column= false;
            lex->alter_password.update_password_expired_fields= true;
            lex->alter_password.use_default_password_lifetime= false;
          }
        | PASSWORD EXPIRE_SYM NEVER_SYM
          {
            LEX *lex= Lex;
            lex->alter_password.expire_after_days= 0;
            lex->alter_password.update_password_expired_column= false;
            lex->alter_password.update_password_expired_fields= true;
            lex->alter_password.use_default_password_lifetime= false;
          }
        | PASSWORD EXPIRE_SYM DEFAULT_SYM
          {
            LEX *lex= Lex;
            lex->alter_password.expire_after_days= 0;
            lex->alter_password.update_password_expired_column= false;
            Lex->alter_password.update_password_expired_fields= true;
            lex->alter_password.use_default_password_lifetime= true;
          }
        | PASSWORD HISTORY_SYM real_ulong_num
          {
            LEX *lex= Lex;
            lex->alter_password.password_history_length= $3;
            lex->alter_password.update_password_history= true;
            lex->alter_password.use_default_password_history= false;
          }
        | PASSWORD HISTORY_SYM DEFAULT_SYM
          {
            LEX *lex= Lex;
            lex->alter_password.password_history_length= 0;
            lex->alter_password.update_password_history= true;
            lex->alter_password.use_default_password_history= true;
          }
        | PASSWORD REUSE_SYM INTERVAL_SYM real_ulong_num DAY_SYM
          {
            LEX *lex= Lex;
            lex->alter_password.password_reuse_interval= $4;
            lex->alter_password.update_password_reuse_interval= true;
            lex->alter_password.use_default_password_reuse_interval= false;
          }
        | PASSWORD REUSE_SYM INTERVAL_SYM DEFAULT_SYM
          {
            LEX *lex= Lex;
            lex->alter_password.password_reuse_interval= 0;
            lex->alter_password.update_password_reuse_interval= true;
            lex->alter_password.use_default_password_reuse_interval= true;
          }
        | PASSWORD REQUIRE_SYM CURRENT_SYM
          {
            LEX *lex= Lex;
            lex->alter_password.update_password_require_current=
                Lex_acl_attrib_udyn::YES;
          }
        | PASSWORD REQUIRE_SYM CURRENT_SYM DEFAULT_SYM
          {
            LEX *lex= Lex;
            lex->alter_password.update_password_require_current=
                Lex_acl_attrib_udyn::DEFAULT;
          }
        | PASSWORD REQUIRE_SYM CURRENT_SYM OPTIONAL_SYM
          {
            LEX *lex= Lex;
            lex->alter_password.update_password_require_current=
                Lex_acl_attrib_udyn::NO;
          }
        | FAILED_LOGIN_ATTEMPTS_SYM real_ulong_num
          {
            LEX *lex= Lex;
            if ($2 > INT_MAX16) {
              char buf[MAX_BIGINT_WIDTH + 1];
              snprintf(buf, sizeof(buf), "%lu", $2);
              my_error(ER_WRONG_VALUE, MYF(0), "FAILED_LOGIN_ATTEMPTS", buf);
              MYSQL_YYABORT;
            }
            lex->alter_password.update_failed_login_attempts= true;
            lex->alter_password.failed_login_attempts= $2;
          }
        | PASSWORD_LOCK_TIME_SYM real_ulong_num
          {
            LEX *lex= Lex;
            if ($2 > INT_MAX16) {
              char buf[MAX_BIGINT_WIDTH + 1];
              snprintf(buf, sizeof(buf), "%lu", $2);
              my_error(ER_WRONG_VALUE, MYF(0), "PASSWORD_LOCK_TIME", buf);
              MYSQL_YYABORT;
            }
            lex->alter_password.update_password_lock_time= true;
            lex->alter_password.password_lock_time= $2;
          }
        | PASSWORD_LOCK_TIME_SYM UNBOUNDED_SYM
          {
            LEX *lex= Lex;
            lex->alter_password.update_password_lock_time= true;
            lex->alter_password.password_lock_time= -1;
          }
        ;

connect_options:
          %empty {}
        | WITH connect_option_list
        ;

connect_option_list:
          connect_option_list connect_option {}
        | connect_option {}
        ;

connect_option:
          MAX_QUERIES_PER_HOUR ulong_num
          {
            LEX *lex=Lex;
            lex->mqh.questions=$2;
            lex->mqh.specified_limits|= USER_RESOURCES::QUERIES_PER_HOUR;
          }
        | MAX_UPDATES_PER_HOUR ulong_num
          {
            LEX *lex=Lex;
            lex->mqh.updates=$2;
            lex->mqh.specified_limits|= USER_RESOURCES::UPDATES_PER_HOUR;
          }
        | MAX_CONNECTIONS_PER_HOUR ulong_num
          {
            LEX *lex=Lex;
            lex->mqh.conn_per_hour= $2;
            lex->mqh.specified_limits|= USER_RESOURCES::CONNECTIONS_PER_HOUR;
          }
        | MAX_USER_CONNECTIONS_SYM ulong_num
          {
            LEX *lex=Lex;
            lex->mqh.user_conn= $2;
            lex->mqh.specified_limits|= USER_RESOURCES::USER_CONNECTIONS;
          }
        ;

user_func:
          USER '(' ')'
          {
            /* empty LEX_USER means current_user */
            LEX_USER *curr_user;
            if (!(curr_user= LEX_USER::alloc(YYTHD)))
              MYSQL_YYABORT;

            Lex->users_list.push_back(curr_user);
            $$= curr_user;
          }
        ;

ev_alter_on_schedule_completion:
          %empty { $$= 0;}
        | ON_SYM SCHEDULE_SYM ev_schedule_time { $$= 1; }
        | ev_on_completion { $$= 1; }
        | ON_SYM SCHEDULE_SYM ev_schedule_time ev_on_completion { $$= 1; }
        ;

opt_alter_table_actions:
          opt_alter_command_list
        | opt_alter_command_list alter_table_partition_options
          {
            $$= $1;
            if ($$.actions == nullptr)
            {
              $$.actions= NEW_PTN Mem_root_array<PT_ddl_table_option *>(YYMEM_ROOT);
              if ($$.actions == nullptr)
                MYSQL_YYABORT; // OOM
            }
            if ($$.actions->push_back($2))
              MYSQL_YYABORT; // OOM
          }
        ;

standalone_alter_table_action:
          standalone_alter_commands
          {
            $$.flags.init();
            $$.action= $1;
          }
        | alter_commands_modifier_list ',' standalone_alter_commands
          {
            $$.flags= $1;
            $$.action= $3;
          }
        ;

alter_table_partition_options:
          partition_clause
          {
            $$= NEW_PTN PT_alter_table_partition_by(@$, $1);
          }
        | REMOVE_SYM PARTITIONING_SYM
          {
            $$= NEW_PTN PT_alter_table_remove_partitioning(@$);
          }
        ;

opt_alter_command_list:
          %empty
          {
            $$.flags.init();
            $$.actions= nullptr;
          }
        | alter_commands_modifier_list
          {
            $$.flags= $1;
            $$.actions= nullptr;
          }
        | alter_list
        | alter_commands_modifier_list ',' alter_list
          {
            $$.flags= $1;
            $$.flags.merge($3.flags);
            $$.actions= $3.actions;
          }
        ;

standalone_alter_commands:
          DISCARD_SYM TABLESPACE_SYM
          {
            $$= NEW_PTN PT_alter_table_discard_tablespace(@$);
          }
        | IMPORT TABLESPACE_SYM
          {
            $$= NEW_PTN PT_alter_table_import_tablespace(@$);
          }
/*
  This part was added for release 5.1 by Mikael Ronström.
  From here we insert a number of commands to manage the partitions of a
  partitioned table such as adding partitions, dropping partitions,
  reorganising partitions in various manners. In future releases the list
  will be longer.
*/
        | ADD PARTITION_SYM opt_no_write_to_binlog
          {
            $$= NEW_PTN PT_alter_table_add_partition(@$, $3);
          }
        | ADD PARTITION_SYM opt_no_write_to_binlog '(' part_def_list ')'
          {
            $$= NEW_PTN PT_alter_table_add_partition_def_list(@$, $3, $5);
          }
        | ADD PARTITION_SYM opt_no_write_to_binlog PARTITIONS_SYM real_ulong_num
          {
            $$= NEW_PTN PT_alter_table_add_partition_num(@$, $3, $5);
          }
        | DROP PARTITION_SYM ident_string_list
          {
            $$= NEW_PTN PT_alter_table_drop_partition(@$, *$3);
          }
        | REBUILD_SYM PARTITION_SYM opt_no_write_to_binlog
          all_or_alt_part_name_list
          {
            $$= NEW_PTN PT_alter_table_rebuild_partition(@$, $3, $4);
          }
        | OPTIMIZE PARTITION_SYM opt_no_write_to_binlog
          all_or_alt_part_name_list
          {
            $$= NEW_PTN PT_alter_table_optimize_partition(@$, $3, $4);
          }
        | ANALYZE_SYM PARTITION_SYM opt_no_write_to_binlog
          all_or_alt_part_name_list
          {
            $$= NEW_PTN PT_alter_table_analyze_partition(@$, $3, $4);
          }
        | CHECK_SYM PARTITION_SYM all_or_alt_part_name_list opt_mi_check_types
          {
            $$= NEW_PTN PT_alter_table_check_partition(@$, $3,
                                                       $4.flags, $4.sql_flags);
          }
        | REPAIR PARTITION_SYM opt_no_write_to_binlog
          all_or_alt_part_name_list
          opt_mi_repair_types
          {
            $$= NEW_PTN PT_alter_table_repair_partition(@$, $3, $4,
                                                        $5.flags, $5.sql_flags);
          }
        | COALESCE PARTITION_SYM opt_no_write_to_binlog real_ulong_num
          {
            $$= NEW_PTN PT_alter_table_coalesce_partition(@$, $3, $4);
          }
        | TRUNCATE_SYM PARTITION_SYM all_or_alt_part_name_list
          {
            $$= NEW_PTN PT_alter_table_truncate_partition(@$, $3);
          }
        | REORGANIZE_SYM PARTITION_SYM opt_no_write_to_binlog
          {
            $$= NEW_PTN PT_alter_table_reorganize_partition(@$, $3);
          }
        | REORGANIZE_SYM PARTITION_SYM opt_no_write_to_binlog
          ident_string_list INTO '(' part_def_list ')'
          {
            $$= NEW_PTN PT_alter_table_reorganize_partition_into(@$, $3, *$4, $7);
          }
        | EXCHANGE_SYM PARTITION_SYM ident
          WITH TABLE_SYM table_ident opt_with_validation
          {
            $$= NEW_PTN PT_alter_table_exchange_partition(@$, $3, $6, $7);
          }
        | DISCARD_SYM PARTITION_SYM all_or_alt_part_name_list
          TABLESPACE_SYM
          {
            $$= NEW_PTN PT_alter_table_discard_partition_tablespace(@$, $3);
          }
        | IMPORT PARTITION_SYM all_or_alt_part_name_list
          TABLESPACE_SYM
          {
            $$= NEW_PTN PT_alter_table_import_partition_tablespace(@$, $3);
          }
        | SECONDARY_LOAD_SYM
          {
            $$= NEW_PTN PT_alter_table_secondary_load(@$);
          }
        | SECONDARY_UNLOAD_SYM
          {
            $$= NEW_PTN PT_alter_table_secondary_unload(@$);
          }
        ;

all_or_alt_part_name_list:
          ALL                   { $$= nullptr; }
        | ident_string_list
        ;

/*
  End of management of partition commands
*/

alter_list:
          alter_list_item
          {
            $$.flags.init();
            $$.actions= NEW_PTN Mem_root_array<PT_ddl_table_option *>(YYMEM_ROOT);
            if ($$.actions == nullptr || $$.actions->push_back($1))
              MYSQL_YYABORT; // OOM
          }
        | alter_list ',' alter_list_item
          {
            if ($$.actions->push_back($3))
              MYSQL_YYABORT; // OOM
          }
        | alter_list ',' alter_commands_modifier
          {
            $$.flags.merge($3);
          }
        | create_table_options_space_separated
          {
            $$.flags.init();
            $$.actions= $1;
          }
        | alter_list ',' create_table_options_space_separated
          {
            for (auto *option : *$3)
            {
              if ($1.actions->push_back(option))
                MYSQL_YYABORT; // OOM
            }
          }
        ;

alter_list_item:
          ADD opt_column ident field_def opt_references opt_place
          {
            $$= NEW_PTN PT_alter_table_add_column(@$, $3, $4, $5, $6);
          }
        | ADD opt_column '(' table_element_list ')'
          {
            $$= NEW_PTN PT_alter_table_add_columns(@$, $4);
          }
        | ADD table_constraint_def
          {
            $$= NEW_PTN PT_alter_table_add_constraint(@$, $2);
          }
        | CHANGE opt_column ident ident field_def opt_place
          {
            $$= NEW_PTN PT_alter_table_change_column(@$, $3, $4, $5, $6);
          }
        | MODIFY_SYM opt_column ident field_def opt_place
          {
            $$= NEW_PTN PT_alter_table_change_column(@$, $3, $4, $5);
          }
        | DROP opt_column ident opt_restrict
          {
            // Note: opt_restrict ($4) is ignored!
            $$= NEW_PTN PT_alter_table_drop_column(@$, $3.str);
          }
        | DROP FOREIGN KEY_SYM ident
          {
            $$= NEW_PTN PT_alter_table_drop_foreign_key(@$, $4.str);
          }
        | DROP PRIMARY_SYM KEY_SYM
          {
            $$= NEW_PTN PT_alter_table_drop_key(@$, primary_key_name);
          }
        | DROP key_or_index ident
          {
            $$= NEW_PTN PT_alter_table_drop_key(@$, $3.str);
          }
        | DROP CHECK_SYM ident
          {
            $$= NEW_PTN PT_alter_table_drop_check_constraint(@$, $3.str);
          }
        | DROP CONSTRAINT ident
          {
            $$= NEW_PTN PT_alter_table_drop_constraint(@$, $3.str);
          }
        | DISABLE_SYM KEYS
          {
            $$= NEW_PTN PT_alter_table_enable_keys(@$, false);
          }
        | ENABLE_SYM KEYS
          {
            $$= NEW_PTN PT_alter_table_enable_keys(@$, true);
          }
        | ALTER opt_column ident SET_SYM DEFAULT_SYM signed_literal_or_null
          {
            $$= NEW_PTN PT_alter_table_set_default(@$, $3.str, $6);
          }
        |  ALTER opt_column ident SET_SYM DEFAULT_SYM '(' expr ')'
          {
            $$= NEW_PTN PT_alter_table_set_default(@$, $3.str, $7);
          }
        | ALTER opt_column ident DROP DEFAULT_SYM
          {
            $$= NEW_PTN PT_alter_table_set_default(@$, $3.str, nullptr);
          }

        | ALTER opt_column ident SET_SYM visibility
          {
            $$= NEW_PTN PT_alter_table_column_visibility(@$, $3.str, $5);
          }
        | ALTER INDEX_SYM ident visibility
          {
            $$= NEW_PTN PT_alter_table_index_visible(@$, $3.str, $4);
          }
        | ALTER CHECK_SYM ident constraint_enforcement
          {
            $$ = NEW_PTN PT_alter_table_enforce_check_constraint(@$, $3.str, $4);
          }
        | ALTER CONSTRAINT ident constraint_enforcement
          {
            $$ = NEW_PTN PT_alter_table_enforce_constraint(@$, $3.str, $4);
          }
        | RENAME opt_to table_ident
          {
            $$= NEW_PTN PT_alter_table_rename(@$, $3);
          }
        | RENAME key_or_index ident TO_SYM ident
          {
            $$= NEW_PTN PT_alter_table_rename_key(@$, $3.str, $5.str);
          }
        | RENAME COLUMN_SYM ident TO_SYM ident
          {
            $$= NEW_PTN PT_alter_table_rename_column(@$, $3.str, $5.str);
          }
        | CONVERT_SYM TO_SYM character_set charset_name opt_collate
          {
            $$= NEW_PTN PT_alter_table_convert_to_charset(@$, $4, $5);
          }
        | CONVERT_SYM TO_SYM character_set DEFAULT_SYM opt_collate
          {
            $$ = NEW_PTN PT_alter_table_convert_to_charset(
                @$,
                YYTHD->variables.collation_database,
                $5 ? $5 : YYTHD->variables.collation_database);
          }
        | FORCE_SYM
          {
            $$= NEW_PTN PT_alter_table_force(@$);
          }
        | ORDER_SYM BY alter_order_list
          {
            $$= NEW_PTN PT_alter_table_order(@$, $3);
          }
        ;

opt_column:
          %empty
        | COLUMN_SYM
        ;

opt_place:
          %empty                { $$= nullptr; }
        | AFTER_SYM ident       { $$= $2.str; }
        | FIRST_SYM             { $$= first_keyword; }
        ;

opt_to:
          %empty {}
        | TO_SYM {}
        | EQ {}
        | AS {}
        ;

group_replication:
          group_replication_start opt_group_replication_start_options
        | STOP_SYM GROUP_REPLICATION
          {
            LEX *lex = Lex;
            lex->sql_command = SQLCOM_STOP_GROUP_REPLICATION;
          }
        ;

group_replication_start:
          START_SYM GROUP_REPLICATION
          {
            LEX *lex = Lex;
            lex->slave_connection.reset();
            lex->sql_command = SQLCOM_START_GROUP_REPLICATION;
          }
        ;

opt_group_replication_start_options:
          %empty
        | group_replication_start_options
        ;

group_replication_start_options:
          group_replication_start_option
        | group_replication_start_options ',' group_replication_start_option
        ;

group_replication_start_option:
          group_replication_user
        | group_replication_password
        | group_replication_plugin_auth
        ;

group_replication_user:
          USER EQ TEXT_STRING_sys_nonewline
          {
            Lex->slave_connection.user = $3.str;
            if ($3.length == 0)
            {
              my_error(ER_GROUP_REPLICATION_USER_EMPTY_MSG, MYF(0));
              MYSQL_YYABORT;
            }
          }
        ;

group_replication_password:
          PASSWORD EQ TEXT_STRING_sys_nonewline
          {
            Lex->slave_connection.password = $3.str;
            Lex->contains_plaintext_password = true;
            if ($3.length > 32)
            {
              my_error(ER_GROUP_REPLICATION_PASSWORD_LENGTH, MYF(0));
              MYSQL_YYABORT;
            }
          }
        ;

group_replication_plugin_auth:
          DEFAULT_AUTH_SYM EQ TEXT_STRING_sys_nonewline
          {
            Lex->slave_connection.plugin_auth= $3.str;
          }
        ;

stop_replica_stmt:
          STOP_SYM replica opt_replica_thread_option_list opt_channel
          {
            LEX *lex=Lex;
            lex->sql_command = SQLCOM_SLAVE_STOP;
            lex->type = 0;
            lex->slave_thd_opt= $3;
            if (lex->is_replication_deprecated_syntax_used())
              push_deprecated_warn(YYTHD, "STOP SLAVE", "STOP REPLICA");
            if (lex->set_channel_name($4))
              MYSQL_YYABORT;  // OOM
          }
        ;

start_replica_stmt:
          START_SYM replica opt_replica_thread_option_list
          {
            LEX *lex=Lex;
            /* Clean previous replica connection values */
            lex->slave_connection.reset();
            lex->sql_command = SQLCOM_SLAVE_START;
            lex->type = 0;
            /* We'll use mi structure for UNTIL options */
            lex->mi.set_unspecified();
            lex->slave_thd_opt= $3;
            if (lex->is_replication_deprecated_syntax_used())
              push_deprecated_warn(YYTHD, "START SLAVE", "START REPLICA");
          }
          opt_replica_until
          opt_user_option opt_password_option
          opt_default_auth_option opt_plugin_dir_option
          {
            /*
              It is not possible to set user's information when
              one is trying to start the SQL Thread.
            */
            if ((Lex->slave_thd_opt & SLAVE_SQL) == SLAVE_SQL &&
                (Lex->slave_thd_opt & SLAVE_IO) != SLAVE_IO &&
                (Lex->slave_connection.user ||
                 Lex->slave_connection.password ||
                 Lex->slave_connection.plugin_auth ||
                 Lex->slave_connection.plugin_dir))
            {
              my_error(ER_SQLTHREAD_WITH_SECURE_REPLICA, MYF(0));
              MYSQL_YYABORT;
            }
          }
          opt_channel
          {
            if (Lex->set_channel_name($11))
              MYSQL_YYABORT;  // OOM
          }
        ;

opt_user_option:
          %empty {}
        | USER EQ TEXT_STRING_sys
          {
            Lex->slave_connection.user= $3.str;
          }
        ;

opt_password_option:
          %empty {}
        | PASSWORD EQ TEXT_STRING_sys
          {
            Lex->slave_connection.password= $3.str;
            Lex->contains_plaintext_password= true;
          }

opt_default_auth_option:
          %empty {}
        | DEFAULT_AUTH_SYM EQ TEXT_STRING_sys
          {
            Lex->slave_connection.plugin_auth= $3.str;
          }
        ;

opt_plugin_dir_option:
          %empty {}
        | PLUGIN_DIR_SYM EQ TEXT_STRING_sys
          {
            Lex->slave_connection.plugin_dir= $3.str;
          }
        ;

opt_replica_thread_option_list:
          %empty
          {
            $$= 0;
          }
        | replica_thread_option_list
          {
            $$= $1;
          }
        ;

replica_thread_option_list:
          replica_thread_option
          {
            $$= $1;
          }
        | replica_thread_option_list ',' replica_thread_option
          {
            $$= $1 | $3;
          }
        ;

replica_thread_option:
          SQL_THREAD
          {
            $$= SLAVE_SQL;
          }
        | RELAY_THREAD
          {
            $$= SLAVE_IO;
          }
        ;

opt_replica_until:
          %empty
          {
            LEX *lex= Lex;
            lex->mi.slave_until= false;
          }
        | UNTIL_SYM replica_until
          {
            LEX *lex=Lex;
            if (((lex->mi.log_file_name || lex->mi.pos) &&
                lex->mi.gtid) ||
               ((lex->mi.relay_log_name || lex->mi.relay_log_pos) &&
                lex->mi.gtid) ||
                !((lex->mi.log_file_name && lex->mi.pos) ||
                  (lex->mi.relay_log_name && lex->mi.relay_log_pos) ||
                  lex->mi.gtid ||
                  lex->mi.until_after_gaps) ||
                /* SQL_AFTER_MTS_GAPS is meaningless in combination */
                /* with any other coordinates related options       */
                ((lex->mi.log_file_name || lex->mi.pos || lex->mi.relay_log_name
                  || lex->mi.relay_log_pos || lex->mi.gtid)
                 && lex->mi.until_after_gaps))
            {
               my_error(ER_BAD_REPLICA_UNTIL_COND, MYF(0));
               MYSQL_YYABORT;
            }
            lex->mi.slave_until= true;
          }
        ;

replica_until:
          source_file_def
        | replica_until ',' source_file_def
        | SQL_BEFORE_GTIDS EQ TEXT_STRING_sys
          {
            Lex->mi.gtid= $3.str;
            Lex->mi.gtid_until_condition= LEX_MASTER_INFO::UNTIL_SQL_BEFORE_GTIDS;
          }
        | SQL_AFTER_GTIDS EQ TEXT_STRING_sys
          {
            Lex->mi.gtid= $3.str;
            Lex->mi.gtid_until_condition= LEX_MASTER_INFO::UNTIL_SQL_AFTER_GTIDS;
          }
        | SQL_AFTER_MTS_GAPS
          {
            Lex->mi.until_after_gaps= true;
          }
        ;

keycache_stmt:
          CACHE_SYM INDEX_SYM keycache_list IN_SYM key_cache_name
          {
            $$= NEW_PTN PT_cache_index_stmt(@$, YYMEM_ROOT, $3, $5);
          }
        | CACHE_SYM INDEX_SYM table_ident adm_partition opt_cache_key_list
          IN_SYM key_cache_name
          {
            $$= NEW_PTN PT_cache_index_partitions_stmt(@$, YYMEM_ROOT,
                                                       $3, $4, $5, $7);
          }
        ;

keycache_list:
          assign_to_keycache
          {
            $$= NEW_PTN Mem_root_array<PT_assign_to_keycache *>(YYMEM_ROOT);
            if ($$ == nullptr || $$->push_back($1))
              MYSQL_YYABORT; // OOM
          }
        | keycache_list ',' assign_to_keycache
          {
            $$= $1;
            if ($$->push_back($3))
              MYSQL_YYABORT; // OOM
          }
        ;

assign_to_keycache:
          table_ident opt_cache_key_list
          {
            $$= NEW_PTN PT_assign_to_keycache(@$, $1, $2);
          }
        ;

key_cache_name:
          ident    { $$= to_lex_cstring($1); }
        | DEFAULT_SYM { $$ = default_key_cache_base; }
        ;

preload_stmt:
          LOAD INDEX_SYM INTO CACHE_SYM
          table_ident adm_partition opt_cache_key_list opt_ignore_leaves
          {
            $$= NEW_PTN PT_load_index_partitions_stmt(@$, YYMEM_ROOT, $5,$6, $7, $8);
          }
        | LOAD INDEX_SYM INTO CACHE_SYM preload_list
          {
            $$= NEW_PTN PT_load_index_stmt(@$, YYMEM_ROOT, $5);
          }
        ;

preload_list:
          preload_keys
          {
            $$= NEW_PTN Mem_root_array<PT_preload_keys *>(YYMEM_ROOT);
            if ($$->push_back($1))
              MYSQL_YYABORT; // OOM
          }
        | preload_list ',' preload_keys
          {
            $$= $1;
            if ($$ == nullptr || $$->push_back($3))
              MYSQL_YYABORT; // OOM
          }
        ;

preload_keys:
          table_ident opt_cache_key_list opt_ignore_leaves
          {
            $$= NEW_PTN PT_preload_keys(@$, $1, $2, $3);
          }
        ;

adm_partition:
          PARTITION_SYM '(' all_or_alt_part_name_list ')'
          {
            $$= NEW_PTN PT_adm_partition(@$, $3);
          }
        ;

opt_cache_key_list:
          %empty { $$= nullptr; }
        | key_or_index '(' opt_key_usage_list ')'
          {
            init_index_hints($3, INDEX_HINT_USE,
                             old_mode ? INDEX_HINT_MASK_JOIN
                                      : INDEX_HINT_MASK_ALL);
            $$= $3;
          }
        ;

opt_ignore_leaves:
          %empty { $$= false; }
        | IGNORE_SYM LEAVES { $$= true; }
        ;

/*
  Order by statement in ALTER TABLE
*/

alter_order_list:
          alter_order_list ',' alter_order_item
          {
            $$= $1;
            $$->push_back($3);
            $$->m_pos = @$;
          }
        | alter_order_item
          {
            $$= NEW_PTN PT_order_list(@$);
            if ($$ == nullptr)
              MYSQL_YYABORT;
            $$->push_back($1);
          }
        ;

alter_order_item:
          simple_ident_nospvar opt_ordering_direction
          {
            $$= NEW_PTN PT_order_expr(@$, $1, $2);
          }
        ;

/* import, export of files */

load_stmt:
          LOAD                          /*  1 */
          data_or_xml                   /*  2 */
          load_data_lock                /*  3 */
          opt_from_keyword              /*  4 */
          opt_local                     /*  5 */
          load_source_type              /*  6 */
          TEXT_STRING_filesystem        /*  7 */
          opt_source_count              /*  8 */
          opt_source_order              /*  9 */
          opt_duplicate                 /* 10 */
          INTO                          /* 11 */
          TABLE_SYM                     /* 12 */
          table_ident                   /* 13 */
          opt_use_partition             /* 14 */
          opt_load_data_charset         /* 15 */
          opt_xml_rows_identified_by    /* 16 */
          opt_field_term                /* 17 */
          opt_line_term                 /* 18 */
          opt_ignore_lines              /* 19 */
          opt_field_or_var_spec         /* 20 */
          opt_load_data_set_spec        /* 21 */
          opt_load_parallel             /* 22 */
          opt_load_memory               /* 23 */
          opt_load_algorithm            /* 24 */
          {
            $$= NEW_PTN PT_load_table(@$, $2,  // data_or_xml
                                      $3,  // load_data_lock
                                      $5,  // opt_local
                                      $6,  // source type
                                      $7,  // TEXT_STRING_filesystem
                                      $8,  // opt_source_count
                                      $9,  // opt_source_order
                                      $10, // opt_duplicate
                                      $13, // table_ident
                                      $14, // opt_use_partition
                                      $15, // opt_load_data_charset
                                      $16, // opt_xml_rows_identified_by
                                      $17, // opt_field_term
                                      $18, // opt_line_term
                                      $19, // opt_ignore_lines
                                      $20, // opt_field_or_var_spec
                                      $21.set_var_list,// opt_load_data_set_spec
                                      $21.set_expr_list,
                                      $21.set_expr_str_list,
                                      $22,  // opt_load_parallel
                                      $23,  // opt_load_memory
                                      $24); // opt_load_algorithm
          }
        ;

data_or_xml:
          DATA_SYM{ $$= FILETYPE_CSV; }
        | XML_SYM { $$= FILETYPE_XML; }
        ;

opt_local:
          %empty      { $$= false; }
        | LOCAL_SYM   { $$= true; }
        ;

opt_from_keyword:
          %empty      {}
        | FROM        {}
        ;

load_data_lock:
          %empty      { $$= TL_WRITE_DEFAULT; }
        | CONCURRENT  { $$= TL_WRITE_CONCURRENT_INSERT; }
        | LOW_PRIORITY { $$= TL_WRITE_LOW_PRIORITY; }
        ;

load_source_type:
          INFILE_SYM { $$ = LOAD_SOURCE_FILE; }
        | URL_SYM    { $$ = LOAD_SOURCE_URL; }
        | S3_SYM     { $$ = LOAD_SOURCE_S3; }
        ;

opt_source_count:
          %empty { $$= 0; }
        | COUNT_SYM NUM { $$= atol($2.str); }
        | IDENT_sys NUM
          {
            // COUNT can be key word or identifier based on SQL mode
            if (my_strcasecmp(system_charset_info, $1.str, "count") != 0) {
              YYTHD->syntax_error_at(@1, "COUNT expected");
              YYABORT;
            }
            $$= atol($2.str);
          }
        ;

opt_source_order:
          %empty { $$= false; }
        | IN_SYM PRIMARY_SYM KEY_SYM ORDER_SYM { $$= true; }
        ;

opt_xml_rows_identified_by:
          %empty { $$= nullptr; }
        | ROWS_SYM IDENTIFIED_SYM BY text_string { $$= $4; }
        ;

opt_ignore_lines:
          %empty { $$= 0; }
        | IGNORE_SYM NUM lines_or_rows  { $$= atol($2.str); }
        ;

lines_or_rows:
          LINES
        | ROWS_SYM
        ;

opt_field_or_var_spec:
          %empty                 { $$= nullptr; }
        | '(' fields_or_vars ')' { $$= $2; }
        | '(' ')'                { $$= nullptr; }
        ;

fields_or_vars:
          fields_or_vars ',' field_or_var
          {
            $$= $1;
            if ($$->push_back($3))
              MYSQL_YYABORT; // OOM
            $$->m_pos = @$;
          }
        | field_or_var
          {
            $$= NEW_PTN PT_item_list(@$);
            if ($$ == nullptr || $$->push_back($1))
              MYSQL_YYABORT; // OOM
          }
        ;

field_or_var:
          simple_ident_nospvar
        | '@' ident_or_text
          {
            $$= NEW_PTN Item_user_var_as_out_param(@$, $2);
          }
        ;

opt_load_data_set_spec:
          %empty { $$= {nullptr, nullptr, nullptr}; }
        | SET_SYM load_data_set_list { $$= $2; }
        ;

load_data_set_list:
          load_data_set_list ',' load_data_set_elem
          {
            $$= $1;
            if ($$.set_var_list->push_back($3.set_var) ||
                $$.set_expr_list->push_back($3.set_expr) ||
                $$.set_expr_str_list->push_back($3.set_expr_str))
              MYSQL_YYABORT; // OOM
          }
        | load_data_set_elem
          {
            $$.set_var_list= NEW_PTN PT_item_list(@$);
            if ($$.set_var_list == nullptr ||
                $$.set_var_list->push_back($1.set_var))
              MYSQL_YYABORT; // OOM

            $$.set_expr_list= NEW_PTN PT_item_list(@$);
            if ($$.set_expr_list == nullptr ||
                $$.set_expr_list->push_back($1.set_expr))
              MYSQL_YYABORT; // OOM

            $$.set_expr_str_list= NEW_PTN List<String>;
            if ($$.set_expr_str_list == nullptr ||
                $$.set_expr_str_list->push_back($1.set_expr_str))
              MYSQL_YYABORT; // OOM
          }
        ;

load_data_set_elem:
          simple_ident_nospvar equal expr_or_default
          {
            size_t length= @3.cpp.end - @2.cpp.start;

            if ($3 == nullptr)
              MYSQL_YYABORT; // OOM
            $3->item_name.copy(@2.cpp.start, length, YYTHD->charset());

            $$.set_var= $1;
            $$.set_expr= $3;
            $$.set_expr_str= NEW_PTN String(@2.cpp.start,
                                            length,
                                            YYTHD->charset());
            if ($$.set_expr_str == nullptr)
              MYSQL_YYABORT; // OOM
          }
        ;

opt_load_algorithm:
          %empty                    { $$ = false; }
        | ALGORITHM_SYM EQ BULK_SYM { $$ = true; }
        ;

opt_load_parallel:
          %empty              { $$ = 0; }
        | PARALLEL_SYM EQ NUM { $$= atol($3.str); }
        ;

opt_load_memory:
          %empty                    { $$ = 0; }
        | MEMORY_SYM EQ size_number { $$ = $3; }
        ;


/**********************************************************************
** Creating different items.
**********************************************************************/

TEXT_STRING_hash:
          TEXT_STRING_sys
        | HEX_NUM
          {
            $$= to_lex_string(Item_hex_string::make_hex_str($1.str, $1.length));
          }
        ;

/*
  SQLCOM_SET_OPTION statement.

  Note that to avoid shift/reduce conflicts, we have separate rules for the
  first option listed in the statement.
*/

set:
          SET_SYM start_option_value_list
          {
            $$= NEW_PTN PT_set(@$, @1, $2);
          }
        ;


// Start of option value list
start_option_value_list:
          option_value_no_option_type option_value_list_continued
          {
            $$= NEW_PTN PT_start_option_value_list_no_type(@$, $1, @1, $2);
          }
        | TRANSACTION_SYM transaction_characteristics
          {
            $$= NEW_PTN PT_start_option_value_list_transaction(@$, $2, @2);
          }
        | option_type start_option_value_list_following_option_type
          {
            $$= NEW_PTN PT_start_option_value_list_type(@$, $1, $2);
          }
        | PASSWORD equal TEXT_STRING_password opt_replace_password opt_retain_current_password
          {
            $$= NEW_PTN PT_option_value_no_option_type_password(@$, $3.str, $4.str,
                                                                $5,
                                                                false,
                                                                @4);
          }
        | PASSWORD TO_SYM RANDOM_SYM opt_replace_password opt_retain_current_password
          {
            // RANDOM PASSWORD GENERATION AND RETURN RESULT SET...
            $$= NEW_PTN PT_option_value_no_option_type_password(@$, $3.str, $4.str,
                                                                $5,
                                                                true,
                                                                @4);
          }
        | PASSWORD FOR_SYM user equal TEXT_STRING_password opt_replace_password opt_retain_current_password
          {
            $$= NEW_PTN PT_option_value_no_option_type_password_for(@$, $3, $5.str,
                                                                    $6.str,
                                                                    $7,
                                                                    false,
                                                                    @6);
          }
        | PASSWORD FOR_SYM user TO_SYM RANDOM_SYM opt_replace_password opt_retain_current_password
          {
            // RANDOM PASSWORD GENERATION AND RETURN RESULT SET...
            $$= NEW_PTN PT_option_value_no_option_type_password_for(@$, $3, $5.str,
                                                                    $6.str,
                                                                    $7,
                                                                    true,
                                                                    @6);
          }
        ;

set_role_stmt:
          SET_SYM ROLE_SYM role_list
          {
            $$= NEW_PTN PT_set_role(@$, $3);
          }
        | SET_SYM ROLE_SYM NONE_SYM
          {
            $$= NEW_PTN PT_set_role(@$, role_enum::ROLE_NONE);
            Lex->sql_command= SQLCOM_SET_ROLE;
          }
        | SET_SYM ROLE_SYM DEFAULT_SYM
          {
            $$= NEW_PTN PT_set_role(@$, role_enum::ROLE_DEFAULT);
            Lex->sql_command= SQLCOM_SET_ROLE;
          }
        | SET_SYM DEFAULT_SYM ROLE_SYM role_list TO_SYM role_list
          {
            $$= NEW_PTN PT_alter_user_default_role(@$, false, $6, $4,
                                                    role_enum::ROLE_NAME);
          }
        | SET_SYM DEFAULT_SYM ROLE_SYM NONE_SYM TO_SYM role_list
          {
            $$= NEW_PTN PT_alter_user_default_role(@$, false, $6, nullptr,
                                                   role_enum::ROLE_NONE);
          }
        | SET_SYM DEFAULT_SYM ROLE_SYM ALL TO_SYM role_list
          {
            $$= NEW_PTN PT_alter_user_default_role(@$, false, $6, nullptr,
                                                   role_enum::ROLE_ALL);
          }
        | SET_SYM ROLE_SYM ALL opt_except_role_list
          {
            $$= NEW_PTN PT_set_role(@$, role_enum::ROLE_ALL, $4);
            Lex->sql_command= SQLCOM_SET_ROLE;
          }
        ;

opt_except_role_list:
          %empty               { $$= nullptr; }
        | EXCEPT_SYM role_list { $$= $2; }
        ;

set_resource_group_stmt:
          SET_SYM RESOURCE_SYM GROUP_SYM ident
          {
            $$= NEW_PTN PT_set_resource_group(@$, to_lex_cstring($4), nullptr);
          }
        | SET_SYM RESOURCE_SYM GROUP_SYM ident FOR_SYM thread_id_list_options
          {
            $$= NEW_PTN PT_set_resource_group(@$, to_lex_cstring($4), $6);
          }
       ;

thread_id_list:
          real_ulong_num
          {
            $$= NEW_PTN Mem_root_array<ulonglong>(YYMEM_ROOT);
            if ($$ == nullptr || $$->push_back($1))
              MYSQL_YYABORT; // OOM
          }
        | thread_id_list opt_comma real_ulong_num
          {
            $$= $1;
            if ($$->push_back($3))
              MYSQL_YYABORT; // OOM
          }
        ;

thread_id_list_options:
         thread_id_list { $$= $1; }
       ;

// Start of option value list, option_type was given
start_option_value_list_following_option_type:
          option_value_following_option_type option_value_list_continued
          {
            $$=
              NEW_PTN PT_start_option_value_list_following_option_type_eq(@$, $1,
                                                                          @1,
                                                                          $2);
          }
        | TRANSACTION_SYM transaction_characteristics
          {
            $$= NEW_PTN
              PT_start_option_value_list_following_option_type_transaction(@$, $2,
                                                                           @2);
          }
        ;

// Remainder of the option value list after first option value.
option_value_list_continued:
          %empty                { $$= nullptr; }
        | ',' option_value_list { $$= $2; }
        ;

// Repeating list of option values after first option value.
option_value_list:
          option_value
          {
            $$= NEW_PTN PT_option_value_list_head(@$, @0, $1, @1);
          }
        | option_value_list ',' option_value
          {
            $$= NEW_PTN PT_option_value_list(@$, $1, @2, $3, @3);
          }
        ;

// Wrapper around option values following the first option value in the stmt.
option_value:
          option_type option_value_following_option_type
          {
            $$= NEW_PTN PT_option_value_type(@$, $1, $2);
          }
        | option_value_no_option_type { $$= $1; }
        ;

option_type:
          GLOBAL_SYM  { $$=OPT_GLOBAL; }
        | PERSIST_SYM { $$=OPT_PERSIST; }
        | PERSIST_ONLY_SYM { $$=OPT_PERSIST_ONLY; }
        | LOCAL_SYM   { $$=OPT_SESSION; }
        | SESSION_SYM { $$=OPT_SESSION; }
        ;

opt_set_var_ident_type:
          %empty          { $$=OPT_DEFAULT; }
        | PERSIST_SYM '.' { $$=OPT_PERSIST; }
        | PERSIST_ONLY_SYM '.' {$$=OPT_PERSIST_ONLY; }
        | GLOBAL_SYM '.'  { $$=OPT_GLOBAL; }
        | LOCAL_SYM '.'   { $$=OPT_SESSION; }
        | SESSION_SYM '.' { $$=OPT_SESSION; }
         ;

// Option values with preceding option_type.
option_value_following_option_type:
          lvalue_variable equal set_expr_or_default
          {
            $$ = NEW_PTN PT_set_scoped_system_variable(
                @$, @1, $1.prefix, $1.name, $3);
          }
        ;

// Option values without preceding option_type.
option_value_no_option_type:
          lvalue_variable equal set_expr_or_default
          {
            $$ = NEW_PTN PT_set_variable(@$, @1, $1.prefix, $1.name, @3, $3);
          }
        | '@' ident_or_text equal expr
          {
            $$= NEW_PTN PT_option_value_no_option_type_user_var(@$, $2, $4);
          }
        | '@' '@' opt_set_var_ident_type lvalue_variable equal
          set_expr_or_default
          {
            $$ = NEW_PTN PT_set_system_variable(
                @$, $3, @4, $4.prefix, $4.name, $6);
          }
        | character_set old_or_new_charset_name_or_default
          {
            $$= NEW_PTN PT_option_value_no_option_type_charset(@$, $2);
          }
        | NAMES_SYM equal expr
          {
            /*
              Bad syntax, always fails with an error
            */
            $$= NEW_PTN PT_option_value_no_option_type_names(@$, @2);
          }
        | NAMES_SYM charset_name opt_collate
          {
            $$= NEW_PTN PT_set_names(@$, $2, $3);
          }
        | NAMES_SYM DEFAULT_SYM
          {
            $$ = NEW_PTN PT_set_names(@$, nullptr, nullptr);
          }
        ;

transaction_characteristics:
          transaction_access_mode opt_isolation_level
          {
            $$= NEW_PTN PT_transaction_characteristics(@$, $1, $2);
          }
        | isolation_level opt_transaction_access_mode
          {
            $$= NEW_PTN PT_transaction_characteristics(@$, $1, $2);
          }
        ;

transaction_access_mode:
          transaction_access_mode_types
          {
            $$= NEW_PTN PT_transaction_access_mode(@$, $1);
          }
        ;

opt_transaction_access_mode:
          %empty { $$= nullptr; }
        | ',' transaction_access_mode { $$= $2; }
        ;

isolation_level:
          ISOLATION LEVEL_SYM isolation_types
          {
            $$= NEW_PTN PT_isolation_level(@$, $3);
          }
        ;

opt_isolation_level:
          %empty { $$= nullptr; }
        | ',' isolation_level { $$= $2; }
        ;

transaction_access_mode_types:
          READ_SYM ONLY_SYM { $$= true; }
        | READ_SYM WRITE_SYM { $$= false; }
        ;

isolation_types:
          READ_SYM UNCOMMITTED_SYM { $$= ISO_READ_UNCOMMITTED; }
        | READ_SYM COMMITTED_SYM   { $$= ISO_READ_COMMITTED; }
        | REPEATABLE_SYM READ_SYM  { $$= ISO_REPEATABLE_READ; }
        | SERIALIZABLE_SYM         { $$= ISO_SERIALIZABLE; }
        ;

set_expr_or_default:
          expr
        | DEFAULT_SYM { $$= nullptr; }
        | ON_SYM
          {
            $$= NEW_PTN Item_string(@$, "ON", 2, system_charset_info);
          }
        | ALL
          {
            $$= NEW_PTN Item_string(@$, "ALL", 3, system_charset_info);
          }
        | BINARY_SYM
          {
            $$= NEW_PTN Item_string(@$, "binary", 6, system_charset_info);
          }
        | ROW_SYM
          {
            $$= NEW_PTN Item_string(@$, "ROW", 3, system_charset_info);
          }
        | SYSTEM_SYM
          {
            $$= NEW_PTN Item_string(@$, "SYSTEM", 6, system_charset_info);
          }
        ;

/*
** Handler: direct access to ISAM functions
*/

handler_stmt:
          HANDLER_SYM table_ident OPEN_SYM opt_table_alias
          {
            $$= NEW_PTN PT_handler_open($2, $4);
          }
        | HANDLER_SYM ident CLOSE_SYM
          {
            $$= NEW_PTN PT_handler_close(to_lex_cstring($2));
          }
        | HANDLER_SYM           /* #1 */
          ident                 /* #2 */
          READ_SYM              /* #3 */
          handler_scan_function /* #4 */
          opt_where_clause      /* #5 */
          opt_limit_clause      /* #6 */
          {
            $$= NEW_PTN PT_handler_table_scan(to_lex_cstring($2), $4, $5, $6);
          }
        | HANDLER_SYM           /* #1 */
          ident                 /* #2 */
          READ_SYM              /* #3 */
          ident                 /* #4 */
          handler_rkey_function /* #5 */
          opt_where_clause      /* #6 */
          opt_limit_clause      /* #7 */
          {
            $$= NEW_PTN PT_handler_index_scan(to_lex_cstring($2),
                                              to_lex_cstring($4), $5, $6, $7);
          }
        | HANDLER_SYM           /* #1 */
          ident                 /* #2 */
          READ_SYM              /* #3 */
          ident                 /* #4 */
          handler_rkey_mode     /* #5 */
          '(' values ')'        /* #6,#7,#8 */
          opt_where_clause      /* #9 */
          opt_limit_clause      /* #10 */
          {
            $$= NEW_PTN PT_handler_index_range_scan(to_lex_cstring($2),
                                                    to_lex_cstring($4),
                                                    $5, $7, $9, $10);
          }
        ;

handler_scan_function:
          FIRST_SYM { $$= enum_ha_read_modes::RFIRST; }
        | NEXT_SYM  { $$= enum_ha_read_modes::RNEXT;  }
        ;

handler_rkey_function:
          FIRST_SYM { $$= enum_ha_read_modes::RFIRST; }
        | NEXT_SYM  { $$= enum_ha_read_modes::RNEXT;  }
        | PREV_SYM  { $$= enum_ha_read_modes::RPREV;  }
        | LAST_SYM  { $$= enum_ha_read_modes::RLAST;  }
        ;

handler_rkey_mode:
          EQ     { $$=HA_READ_KEY_EXACT;   }
        | GE     { $$=HA_READ_KEY_OR_NEXT; }
        | LE     { $$=HA_READ_KEY_OR_PREV; }
        | GT_SYM { $$=HA_READ_AFTER_KEY;   }
        | LT     { $$=HA_READ_BEFORE_KEY;  }
        ;

opt_and:
          %empty
        | AND_SYM
        ;

require_list:
          require_list_element opt_and require_list
        | require_list_element
        ;

require_list_element:
          SUBJECT_SYM TEXT_STRING
          {
            LEX *lex=Lex;
            if (lex->x509_subject)
            {
              my_error(ER_DUP_ARGUMENT, MYF(0), "SUBJECT");
              MYSQL_YYABORT;
            }
            lex->x509_subject=$2.str;
          }
        | ISSUER_SYM TEXT_STRING
          {
            LEX *lex=Lex;
            if (lex->x509_issuer)
            {
              my_error(ER_DUP_ARGUMENT, MYF(0), "ISSUER");
              MYSQL_YYABORT;
            }
            lex->x509_issuer=$2.str;
          }
        | CIPHER_SYM TEXT_STRING
          {
            LEX *lex=Lex;
            if (lex->ssl_cipher)
            {
              my_error(ER_DUP_ARGUMENT, MYF(0), "CIPHER");
              MYSQL_YYABORT;
            }
            lex->ssl_cipher=$2.str;
          }
        ;

opt_retain_current_password:
          %empty { $$= false; }
        | RETAIN_SYM CURRENT_SYM PASSWORD { $$= true; }
        ;

opt_discard_old_password:
          %empty { $$= false; }
        | DISCARD_SYM OLD_SYM PASSWORD { $$= true; }


opt_user_registration:
          factor INITIATE_SYM REGISTRATION_SYM
          {
            LEX_MFA *m = NEW_PTN LEX_MFA;
            if (m == nullptr)
              MYSQL_YYABORT;  // OOM
            m->nth_factor= $1;
            m->init_registration= true;
            m->requires_registration= true;
            $$ = m;
          }
        | factor UNREGISTER_SYM
          {
            LEX_MFA *m = NEW_PTN LEX_MFA;
            if (m == nullptr)
              MYSQL_YYABORT;  // OOM
            m->nth_factor= $1;
            m->unregister= true;
            $$ = m;
          }
        | factor FINISH_SYM REGISTRATION_SYM SET_SYM CHALLENGE_RESPONSE_SYM AS TEXT_STRING_hash
          {
            LEX_MFA *m = NEW_PTN LEX_MFA;
            if (m == nullptr)
              MYSQL_YYABORT;  // OOM
            m->nth_factor= $1;
            m->finish_registration= true;
            m->requires_registration= true;
            m->challenge_response= to_lex_cstring($7);
            $$ = m;
          }
        ;

create_user:
          user identification opt_create_user_with_mfa
          {
            $$ = $1;
            $$->first_factor_auth_info = *$2;
            if ($$->add_mfa_identifications($3.mfa2, $3.mfa3))
              MYSQL_YYABORT;  // OOM
          }
        | user identified_with_plugin opt_initial_auth
          {
            $$= $1;
            /* set $3 as first factor auth method */
            $3->nth_factor = 1;
            $3->passwordless = false;
            $$->first_factor_auth_info = *$3;
            /* set $2 as second factor auth method */
            $2->nth_factor = 2;
            $2->passwordless = true;
            if ($$->mfa_list.push_back($2))
              MYSQL_YYABORT;  // OOM
            $$->with_initial_auth = true;
          }
        | user opt_create_user_with_mfa
          {
            $$ = $1;
            if ($$->add_mfa_identifications($2.mfa2, $2.mfa3))
              MYSQL_YYABORT;  // OOM
          }
        ;

opt_create_user_with_mfa:
          %empty { $$ = {}; }
        | AND_SYM identification
          {
            $2->nth_factor = 2;
            $$ = {$2, nullptr};
          }
        | AND_SYM identification AND_SYM identification
          {
            $2->nth_factor = 2;
            $4->nth_factor = 3;
            $$ = {$2, $4};
          }
        ;

identification:
          identified_by_password
        | identified_by_random_password
        | identified_with_plugin
        | identified_with_plugin_as_auth
        | identified_with_plugin_by_password
        | identified_with_plugin_by_random_password
        ;

identified_by_password:
          IDENTIFIED_SYM BY TEXT_STRING_password
          {
            LEX_MFA *m = NEW_PTN LEX_MFA;
            if (m == nullptr)
              MYSQL_YYABORT;  // OOM
            m->auth = to_lex_cstring($3);
            m->uses_identified_by_clause = true;
            $$ = m;
            Lex->contains_plaintext_password= true;
          }
        ;

identified_by_random_password:
          IDENTIFIED_SYM BY RANDOM_SYM PASSWORD
          {
            LEX_MFA *m = NEW_PTN LEX_MFA;
            if (m == nullptr)
              MYSQL_YYABORT;  // OOM
            m->auth = EMPTY_CSTR;
            m->has_password_generator = true;
            m->uses_identified_by_clause = true;
            $$ = m;
            Lex->contains_plaintext_password = true;
          }
        ;

identified_with_plugin:
          IDENTIFIED_SYM WITH ident_or_text
          {
            LEX_MFA *m = NEW_PTN LEX_MFA;
            if (m == nullptr)
              MYSQL_YYABORT;  // OOM
            m->plugin = to_lex_cstring($3);
            m->auth = EMPTY_CSTR;
            m->uses_identified_by_clause = false;
            m->uses_identified_with_clause = true;
            $$ = m;
          }
        ;

identified_with_plugin_as_auth:
          IDENTIFIED_SYM WITH ident_or_text AS TEXT_STRING_hash
          {
            LEX_MFA *m = NEW_PTN LEX_MFA;
            if (m == nullptr)
              MYSQL_YYABORT;  // OOM
            m->plugin = to_lex_cstring($3);
            m->auth = to_lex_cstring($5);
            m->uses_authentication_string_clause = true;
            m->uses_identified_with_clause = true;
            $$ = m;
          }
        ;

identified_with_plugin_by_password:
          IDENTIFIED_SYM WITH ident_or_text BY TEXT_STRING_password
          {
            LEX_MFA *m = NEW_PTN LEX_MFA;
            if (m == nullptr)
              MYSQL_YYABORT;  // OOM
            m->plugin = to_lex_cstring($3);
            m->auth = to_lex_cstring($5);
            m->uses_identified_by_clause = true;
            m->uses_identified_with_clause = true;
            $$ = m;
            Lex->contains_plaintext_password= true;
          }
        ;

identified_with_plugin_by_random_password:
          IDENTIFIED_SYM WITH ident_or_text BY RANDOM_SYM PASSWORD
          {
            LEX_MFA *m = NEW_PTN LEX_MFA;
            if (m == nullptr)
              MYSQL_YYABORT;  // OOM
            m->plugin = to_lex_cstring($3);
            m->uses_identified_by_clause = true;
            m->uses_identified_with_clause = true;
            m->has_password_generator = true;
            $$ = m;
            Lex->contains_plaintext_password= true;
          }
        ;

opt_initial_auth:
          INITIAL_SYM AUTHENTICATION_SYM identified_by_random_password
           {
            $$ = $3;
            $3->passwordless = true;
            $3->nth_factor = 2;
          }
        | INITIAL_SYM AUTHENTICATION_SYM identified_with_plugin_as_auth
          {
            $$ = $3;
            $3->passwordless = true;
            $3->nth_factor = 2;
          }
        | INITIAL_SYM AUTHENTICATION_SYM identified_by_password
          {
            $$ = $3;
            $3->passwordless = true;
            $3->nth_factor = 2;
          }
        ;

alter_user:
          user identified_by_password
          REPLACE_SYM TEXT_STRING_password
          opt_retain_current_password
          {
            $$ = $1;
            $1->first_factor_auth_info = *$2;
            $1->current_auth = to_lex_cstring($4);
            $1->uses_replace_clause = true;
            $1->discard_old_password = false;
            $1->retain_current_password = $5;
          }
        | user identified_with_plugin_by_password
          REPLACE_SYM TEXT_STRING_password
          opt_retain_current_password
          {
            $$ = $1;
            $1->first_factor_auth_info = *$2;
            $1->current_auth = to_lex_cstring($4);
            $1->uses_replace_clause = true;
            $1->discard_old_password = false;
            $1->retain_current_password = $5;
          }
        | user identified_by_password opt_retain_current_password
          {
            $$ = $1;
            $1->first_factor_auth_info = *$2;
            $1->discard_old_password = false;
            $1->retain_current_password = $3;
          }
        | user identified_by_random_password opt_retain_current_password
           {
            $$ = $1;
            $1->first_factor_auth_info = *$2;
            $1->discard_old_password = false;
            $1->retain_current_password = $3;
          }
        | user identified_by_random_password
          REPLACE_SYM TEXT_STRING_password
          opt_retain_current_password
          {
            $$ = $1;
            $1->first_factor_auth_info = *$2;
            $1->uses_replace_clause = true;
            $1->discard_old_password = false;
            $1->retain_current_password = $5;
            $1->current_auth = to_lex_cstring($4);
          }
        | user identified_with_plugin
          {
            $$ = $1;
            $1->first_factor_auth_info = *$2;
            $1->discard_old_password = false;
            $1->retain_current_password = false;
          }
        | user identified_with_plugin_as_auth opt_retain_current_password
          {
            $$ = $1;
            $1->first_factor_auth_info = *$2;
            $1->discard_old_password = false;
            $1->retain_current_password = $3;
          }
        | user identified_with_plugin_by_password opt_retain_current_password
          {
            $$ = $1;
            $1->first_factor_auth_info = *$2;
            $1->discard_old_password = false;
            $1->retain_current_password = $3;
          }
        | user identified_with_plugin_by_random_password
          opt_retain_current_password
          {
            $$ = $1;
            $1->first_factor_auth_info = *$2;
            $1->discard_old_password= false;
            $1->retain_current_password= $3;
          }
        | user opt_discard_old_password
          {
            $$ = $1;
            $1->discard_old_password = $2;
            $1->retain_current_password = false;
          }
        | user ADD factor identification
          {
            $4->nth_factor = $3;
            $4->add_factor = true;
            if ($1->add_mfa_identifications($4))
              MYSQL_YYABORT;  // OOM
            $$ = $1;
           }
        | user ADD factor identification ADD factor identification
          {
            if ($3 == $6) {
              my_error(ER_MFA_METHODS_IDENTICAL, MYF(0));
              MYSQL_YYABORT;
            } else if ($3 > $6) {
              my_error(ER_MFA_METHODS_INVALID_ORDER, MYF(0), $6, $3);
              MYSQL_YYABORT;
            }
            $4->nth_factor = $3;
            $4->add_factor = true;
            $7->nth_factor = $6;
            $7->add_factor = true;
            if ($1->add_mfa_identifications($4, $7))
              MYSQL_YYABORT;  // OOM
            $$ = $1;
          }
        | user MODIFY_SYM factor identification
          {
            $4->nth_factor = $3;
            $4->modify_factor = true;
            if ($1->add_mfa_identifications($4))
              MYSQL_YYABORT;  // OOM
            $$ = $1;
           }
        | user MODIFY_SYM factor identification MODIFY_SYM factor identification
          {
            if ($3 == $6) {
              my_error(ER_MFA_METHODS_IDENTICAL, MYF(0));
              MYSQL_YYABORT;
            }
            $4->nth_factor = $3;
            $4->modify_factor = true;
            $7->nth_factor = $6;
            $7->modify_factor = true;
            if ($1->add_mfa_identifications($4, $7))
              MYSQL_YYABORT;  // OOM
            $$ = $1;
          }
        | user DROP factor
          {
            LEX_MFA *m = NEW_PTN LEX_MFA;
            if (m == nullptr)
              MYSQL_YYABORT;  // OOM
            m->nth_factor = $3;
            m->drop_factor = true;
            if ($1->add_mfa_identifications(m))
              MYSQL_YYABORT;  // OOM
            $$ = $1;
           }
        | user DROP factor DROP factor
          {
            if ($3 == $5) {
              my_error(ER_MFA_METHODS_IDENTICAL, MYF(0));
              MYSQL_YYABORT;
            }
            LEX_MFA *m1 = NEW_PTN LEX_MFA;
            if (m1 == nullptr)
              MYSQL_YYABORT;  // OOM
            m1->nth_factor = $3;
            m1->drop_factor = true;
            LEX_MFA *m2 = NEW_PTN LEX_MFA;
            if (m2 == nullptr)
              MYSQL_YYABORT;  // OOM
            m2->nth_factor = $5;
            m2->drop_factor = true;
            if ($1->add_mfa_identifications(m1, m2))
              MYSQL_YYABORT;  // OOM
            $$ = $1;
           }
         ;

factor:
          NUM FACTOR_SYM
          {
            if (my_strcasecmp(system_charset_info, $1.str, "2") == 0) {
              $$ = 2;
            } else if (my_strcasecmp(system_charset_info, $1.str, "3") == 0) {
              $$ = 3;
            } else {
               my_error(ER_WRONG_VALUE, MYF(0), "nth factor", $1.str);
               MYSQL_YYABORT;
            }
          }
        ;

create_user_list:
          create_user
          {
            if (Lex->users_list.push_back($1))
              MYSQL_YYABORT;
          }
        | create_user_list ',' create_user
          {
            if (Lex->users_list.push_back($3))
              MYSQL_YYABORT;
          }
        ;

alter_user_list:
       alter_user
         {
            if (Lex->users_list.push_back($1))
              MYSQL_YYABORT;
         }
       | alter_user_list ',' alter_user
          {
            if (Lex->users_list.push_back($3))
              MYSQL_YYABORT;
          }
        ;

require_clause:
          %empty
        | REQUIRE_SYM require_list
          {
            Lex->ssl_type=SSL_TYPE_SPECIFIED;
          }
        | REQUIRE_SYM SSL_SYM
          {
            Lex->ssl_type=SSL_TYPE_ANY;
          }
        | REQUIRE_SYM X509_SYM
          {
            Lex->ssl_type=SSL_TYPE_X509;
          }
        | REQUIRE_SYM NONE_SYM
          {
            Lex->ssl_type=SSL_TYPE_NONE;
          }
        ;

/**************************************************************************

 CREATE VIEW | TRIGGER | PROCEDURE statements.

**************************************************************************/

init_lex_create_info:
          %empty
          {
            // Initialize context for 'CREATE view_or_trigger_or_sp_or_event'
            Lex->create_info= YYTHD->alloc_typed<HA_CREATE_INFO>();
            if (Lex->create_info == nullptr)
              MYSQL_YYABORT; // OOM
          }
        ;

view_or_trigger_or_sp_or_event:
          definer init_lex_create_info definer_tail
          {}
        | no_definer init_lex_create_info no_definer_tail
          {}
        | view_replace_or_algorithm definer_opt init_lex_create_info view_tail
          {}
        ;

definer_tail:
          view_tail
        | trigger_tail
        | sp_tail
        | sf_tail
        | event_tail
        ;

no_definer_tail:
          view_tail
        | trigger_tail
        | sp_tail
        | sf_tail
        | udf_tail
        | event_tail
        ;

/**************************************************************************

 CREATE VIEW statement parts.

**************************************************************************/

view_replace_or_algorithm:
          view_replace
          {}
        | view_replace view_algorithm
          {}
        | view_algorithm
          {}
        ;

view_replace:
          OR_SYM REPLACE_SYM
          { Lex->create_view_mode= enum_view_create_mode::VIEW_CREATE_OR_REPLACE; }
        ;

view_algorithm:
          ALGORITHM_SYM EQ UNDEFINED_SYM
          { Lex->create_view_algorithm= VIEW_ALGORITHM_UNDEFINED; }
        | ALGORITHM_SYM EQ MERGE_SYM
          { Lex->create_view_algorithm= VIEW_ALGORITHM_MERGE; }
        | ALGORITHM_SYM EQ TEMPTABLE_SYM
          { Lex->create_view_algorithm= VIEW_ALGORITHM_TEMPTABLE; }
        ;

view_suid:
          %empty { Lex->create_view_suid= VIEW_SUID_DEFAULT; }
        | SQL_SYM SECURITY_SYM DEFINER_SYM
          { Lex->create_view_suid= VIEW_SUID_DEFINER; }
        | SQL_SYM SECURITY_SYM INVOKER_SYM
          { Lex->create_view_suid= VIEW_SUID_INVOKER; }
        ;

view_tail:
          view_suid VIEW_SYM table_ident opt_derived_column_list
          {
            THD *thd= YYTHD;
            LEX *lex= thd->lex;
            lex->sql_command= SQLCOM_CREATE_VIEW;
            /* first table in list is target VIEW name */
            if (!lex->query_block->add_table_to_list(thd, $3, nullptr,
                                                    TL_OPTION_UPDATING,
                                                    TL_IGNORE,
                                                    MDL_EXCLUSIVE))
              MYSQL_YYABORT;
            lex->query_tables->open_strategy= Table_ref::OPEN_STUB;
            thd->parsing_system_view= lex->query_tables->is_system_view;
            if ($4.size())
            {
              for (auto column_alias : $4)
              {
                // Report error if the column name/length is incorrect.
                if (check_column_name(column_alias.str))
                {
                  my_error(ER_WRONG_COLUMN_NAME, MYF(0), column_alias.str);
                  MYSQL_YYABORT;
                }
              }
              /*
                The $4 object is short-lived (its 'm_array' is not);
                so we have to duplicate it, and then we can store a
                pointer.
              */
              void *rawmem= thd->memdup(&($4), sizeof($4));
              if (!rawmem)
                MYSQL_YYABORT; /* purecov: inspected */
              lex->query_tables->
                set_derived_column_names(static_cast<Create_col_name_list* >(rawmem));
            }
          }
          AS view_query_block
        ;

view_query_block:
          query_expression_with_opt_locking_clauses view_check_option
          {
            THD *thd= YYTHD;
            LEX *lex= Lex;
            lex->parsing_options.allows_variable= false;
            lex->parsing_options.allows_select_into= false;

            /*
              In CREATE VIEW v ... the m_table_list initially contains
              here a table entry for the destination "table" `v'.
              Backup it and clean the table list for the processing of
              the query expression and push `v' back to the beginning of the
              m_table_list finally.

              The following work only with the local list, the global list
              is created correctly in this case
            */
            SQL_I_List<Table_ref> save_list;
            Query_block * const save_query_block= Select;
            save_query_block->m_table_list.save_and_clear(&save_list);

            CONTEXTUALIZE_VIEW($1);

            /*
              The following work only with the local list, the global list
              is created correctly in this case
            */
            save_query_block->m_table_list.push_front(&save_list);

            Lex->create_view_check= $2;

            /*
              It's simpler to use @$ to grab the whole rule text, OTOH  it's
              also simple to lose something that way when changing this rule,
              so let use explicit @1 and @2 to memdup this view definition:
            */
            const size_t len= @2.cpp.end - @1.cpp.start;
            lex->create_view_query_block.str=
              static_cast<char *>(thd->memdup(@1.cpp.start, len));
            lex->create_view_query_block.length= len;
            trim_whitespace(thd->charset(), &lex->create_view_query_block);

            lex->parsing_options.allows_variable= true;
            lex->parsing_options.allows_select_into= true;
          }
        ;

/**************************************************************************

 CREATE TRIGGER statement parts.

**************************************************************************/

trigger_action_order:
            FOLLOWS_SYM
            { $$= TRG_ORDER_FOLLOWS; }
          | PRECEDES_SYM
            { $$= TRG_ORDER_PRECEDES; }
          ;

trigger_follows_precedes_clause:
            %empty
            {
              $$.ordering_clause= TRG_ORDER_NONE;
              $$.anchor_trigger_name= NULL_CSTR;
            }
          |
            trigger_action_order ident_or_text
            {
              $$.ordering_clause= $1;
              $$.anchor_trigger_name= { $2.str, $2.length };
            }
          ;

trigger_tail:
          TRIGGER_SYM                     /* $1 */
          opt_if_not_exists               /* $2 */
          sp_name                         /* $3 */
          trg_action_time                 /* $4 */
          trg_event                       /* $5 */
          ON_SYM                          /* $6 */
          table_ident                     /* $7 */
          FOR_SYM                         /* $8 */
          EACH_SYM                        /* $9 */
          ROW_SYM                         /* $10 */
          trigger_follows_precedes_clause /* $11 */
          {                               /* $12 */
            THD *thd= YYTHD;
            LEX *lex= thd->lex;

            if (lex->sphead)
            {
              my_error(ER_SP_NO_RECURSIVE_CREATE, MYF(0), "TRIGGER");
              MYSQL_YYABORT;
            }

            sp_head *sp= sp_start_parsing(thd, enum_sp_type::TRIGGER, $3);

            if (!sp)
              MYSQL_YYABORT;

            sp->m_trg_chistics.action_time= (enum enum_trigger_action_time_type) $4;
            sp->m_trg_chistics.event= (enum enum_trigger_event_type) $5;
            sp->m_trg_chistics.ordering_clause= $11.ordering_clause;
            sp->m_trg_chistics.anchor_trigger_name= $11.anchor_trigger_name;

            lex->stmt_definition_begin= @1.cpp.start;
            lex->create_info->options= $2 ? HA_LEX_CREATE_IF_NOT_EXISTS : 0;
            lex->ident.str= const_cast<char *>(@7.cpp.start);
            lex->ident.length= @9.cpp.start - @7.cpp.start;

            lex->sphead= sp;
            lex->spname= $3;

            memset(&lex->sp_chistics, 0, sizeof(st_sp_chistics));
            sp->m_chistics= &lex->sp_chistics;

            // Default language is SQL
            lex->sp_chistics.language = {"SQL",3};

            sp->set_body_start(thd, @11.cpp.end);
          }
          sp_proc_stmt                    /* $13 */
          {                               /* $14 */
            THD *thd= YYTHD;
            LEX *lex= Lex;
            sp_head *sp= lex->sphead;

            sp_finish_parsing(thd);

            lex->sql_command= SQLCOM_CREATE_TRIGGER;

            if (sp->is_not_allowed_in_function("trigger"))
              MYSQL_YYABORT;

            /*
              We have to do it after parsing trigger body, because some of
              sp_proc_stmt alternatives are not saving/restoring LEX, so
              lex->query_tables can be wiped out.
            */
            if (!lex->query_block->add_table_to_list(thd, $7,
                                                    nullptr,
                                                    TL_OPTION_UPDATING,
                                                    TL_READ_NO_INSERT,
                                                    MDL_SHARED_NO_WRITE))
              MYSQL_YYABORT;

            Lex->m_sql_cmd= new (YYTHD->mem_root) Sql_cmd_create_trigger();
          }
        ;

/**************************************************************************

 CREATE FUNCTION | PROCEDURE statements parts.

**************************************************************************/

udf_tail:
          AGGREGATE_SYM         /* $1 */
          FUNCTION_SYM          /* $2 */
          opt_if_not_exists     /* $3 */
          ident                 /* $4 */
          RETURNS_SYM           /* $5 */
          udf_type              /* $6 */
          SONAME_SYM            /* $7 */
          TEXT_STRING_sys       /* $8 */
          {                     /* $9 */
            THD *thd= YYTHD;
            LEX *lex= thd->lex;

            if (is_native_function($4))
            {
              if($3)
              {
                /*
                  IF NOT EXISTS clause is unsupported when creating a UDF with
                  the same name as a native function
                */
                my_error(ER_IF_NOT_EXISTS_UNSUPPORTED_UDF_NATIVE_FCT_NAME_COLLISION, MYF(0), $4.str);
              }
              else
                my_error(ER_NATIVE_FCT_NAME_COLLISION, MYF(0), $4.str);
              MYSQL_YYABORT;
            }
            lex->sql_command = SQLCOM_CREATE_FUNCTION;
            lex->udf.type= UDFTYPE_AGGREGATE;
            lex->stmt_definition_begin= @2.cpp.start;
            lex->create_info->options= $3 ? HA_LEX_CREATE_IF_NOT_EXISTS : 0;
            lex->udf.name = $4;
            lex->udf.returns=(Item_result) $6;
            lex->udf.dl=$8.str;
          }
        | FUNCTION_SYM          /* $1 */
          opt_if_not_exists     /* $2 */
          ident                 /* $3 */
          RETURNS_SYM           /* $4 */
          udf_type              /* $5 */
          SONAME_SYM            /* $6 */
          TEXT_STRING_sys       /* $7 */
          {
            THD *thd= YYTHD;
            LEX *lex= thd->lex;

            if (is_native_function($3))
            {
              if($2)
              {
                /*
                  IF NOT EXISTS clause is unsupported when creating a UDF with
                  the same name as a native function
                */
                my_error(ER_IF_NOT_EXISTS_UNSUPPORTED_UDF_NATIVE_FCT_NAME_COLLISION, MYF(0), $3.str);
              }
              else
                my_error(ER_NATIVE_FCT_NAME_COLLISION, MYF(0), $3.str);
              MYSQL_YYABORT;
            }
            lex->sql_command = SQLCOM_CREATE_FUNCTION;
            lex->udf.type= UDFTYPE_FUNCTION;
            lex->stmt_definition_begin= @1.cpp.start;
            lex->create_info->options= $2 ? HA_LEX_CREATE_IF_NOT_EXISTS : 0;
            lex->udf.name = $3;
            lex->udf.returns=(Item_result) $5;
            lex->udf.dl=$7.str;
          }
        ;

sf_tail:
          FUNCTION_SYM          /* $1 */
          opt_if_not_exists     /* $2 */
          sp_name               /* $3 */
          '('                   /* $4 */
          {                     /* $5 */
            THD *thd= YYTHD;
            LEX *lex= thd->lex;

            lex->stmt_definition_begin= @1.cpp.start;
            lex->spname= $3;

            if (lex->sphead)
            {
              my_error(ER_SP_NO_RECURSIVE_CREATE, MYF(0), "FUNCTION");
              MYSQL_YYABORT;
            }


            sp_head *sp= sp_start_parsing(thd, enum_sp_type::FUNCTION, lex->spname);

            if (!sp)
              MYSQL_YYABORT;

            lex->sphead= sp;
            lex->create_info->options= $2 ? HA_LEX_CREATE_IF_NOT_EXISTS : 0;

            sp->m_parser_data.set_parameter_start_ptr(@4.cpp.end);
          }
          sp_fdparam_list       /* $6 */
          ')'                   /* $7 */
          {                     /* $8 */
            Lex->sphead->m_parser_data.set_parameter_end_ptr(@7.cpp.start);
          }
          RETURNS_SYM           /* $9 */
          type                  /* $10 */
          opt_collate           /* $11 */
          {                     /* $12 */
            LEX *lex= Lex;
            sp_head *sp= lex->sphead;

            CONTEXTUALIZE($10);
            enum_field_types field_type= $10->type;
            const CHARSET_INFO *cs= $10->get_charset();
            if (merge_sp_var_charset_and_collation(cs, $11, &cs))
              MYSQL_YYABORT;

            /*
              This was disabled in 5.1.12. See bug #20701
              When collation support in SP is implemented, then this test
              should be removed.
            */
            if ((field_type == MYSQL_TYPE_STRING || field_type == MYSQL_TYPE_VARCHAR)
                && ($10->get_type_flags() & BINCMP_FLAG))
            {
              my_error(ER_NOT_SUPPORTED_YET, MYF(0), "return value collation");
              MYSQL_YYABORT;
            }

            if (sp->m_return_field_def.init(YYTHD, "", field_type,
                                            $10->get_length(), $10->get_dec(),
                                            $10->get_type_flags(), nullptr, nullptr, &NULL_CSTR, nullptr,
                                            $10->get_interval_list(),
                                            cs ? cs : YYTHD->variables.collation_database,
                                            $11 != nullptr, $10->get_uint_geom_type(),
                                            nullptr, nullptr, {},
                                            dd::Column::enum_hidden_type::HT_VISIBLE))
            {
              MYSQL_YYABORT;
            }

            if (prepare_sp_create_field(YYTHD,
                                        &sp->m_return_field_def))
              MYSQL_YYABORT;

            memset(&lex->sp_chistics, 0, sizeof(st_sp_chistics));

            // Default language is SQL
            lex->sp_chistics.language = {"SQL",3};
          }
          sp_c_chistics         /* $13 */
          {                     /* $14 */
            THD *thd= YYTHD;
            LEX *lex= thd->lex;

            lex->sphead->m_chistics= &lex->sp_chistics;
            lex->sphead->set_body_start(thd, yylloc.cpp.start);
          }
          stored_routine_body   /* $15 */
          {
            THD *thd= YYTHD;
            LEX *lex= thd->lex;
            sp_head *sp= lex->sphead;

            if (sp->is_not_allowed_in_function("function"))
              MYSQL_YYABORT;

            lex->sql_command= SQLCOM_CREATE_SPFUNCTION;

            if (sp->is_sql() && !(sp->m_flags & sp_head::HAS_RETURN)) {
              my_error(ER_SP_NORETURN, MYF(0), sp->m_qname.str);
              MYSQL_YYABORT;
            }

            if (is_native_function(sp->m_name))
            {
              /*
                This warning will be printed when
                [1] A client query is parsed,
                [2] A stored function is loaded by db_load_routine.
                Printing the warning for [2] is intentional, to cover the
                following scenario:
                - A user define a SF 'foo' using MySQL 5.N
                - An application uses select foo(), and works.
                - MySQL 5.{N+1} defines a new native function 'foo', as
                part of a new feature.
                - MySQL 5.{N+1} documentation is updated, and should mention
                that there is a potential incompatible change in case of
                existing stored function named 'foo'.
                - The user deploys 5.{N+1}. At this point, 'select foo()'
                means something different, and the user code is most likely
                broken (it's only safe if the code is 'select db.foo()').
                With a warning printed when the SF is loaded (which has to occur
                before the call), the warning will provide a hint explaining
                the root cause of a later failure of 'select foo()'.
                With no warning printed, the user code will fail with no
                apparent reason.
                Printing a warning each time db_load_routine is executed for
                an ambiguous function is annoying, since that can happen a lot,
                but in practice should not happen unless there *are* name
                collisions.
                If a collision exists, it should not be silenced but fixed.
              */
              push_warning_printf(thd,
                                  Sql_condition::SL_NOTE,
                                  ER_NATIVE_FCT_NAME_COLLISION,
                                  ER_THD(thd, ER_NATIVE_FCT_NAME_COLLISION),
                                  sp->m_name.str);
            }
          }
        ;

routine_string:
          TEXT_STRING_literal
        | DOLLAR_QUOTED_STRING_SYM

stored_routine_body:
          AS routine_string
          {
            sp_head *sp = Lex->sphead;
            if (sp->is_sql()) {
               YYTHD->syntax_error();
               MYSQL_YYABORT;
            }
            sp->code = to_lex_cstring($2);

            THD *thd = YYTHD;
            sp_finish_parsing(thd);
          }
        | sp_proc_stmt
          {
            if (!Lex->sphead->is_sql()) {
              YYTHD->syntax_error();
              MYSQL_YYABORT;
            }

            THD *thd = YYTHD;
            sp_finish_parsing(thd);
          }
        ;

sp_tail:
          PROCEDURE_SYM         /*$1*/
          opt_if_not_exists     /*$2*/
          sp_name               /*$3*/
          {                     /*$4*/
            THD *thd= YYTHD;
            LEX *lex= Lex;

            if (lex->sphead)
            {
              my_error(ER_SP_NO_RECURSIVE_CREATE, MYF(0), "PROCEDURE");
              MYSQL_YYABORT;
            }

            lex->stmt_definition_begin= @1.cpp.start;

            sp_head *sp= sp_start_parsing(thd, enum_sp_type::PROCEDURE, $3);

            if (!sp)
              MYSQL_YYABORT;

            lex->sphead= sp;
            lex->create_info->options= $2 ? HA_LEX_CREATE_IF_NOT_EXISTS : 0;
          }
          '('                   /*$5*/
          {                     /*$6*/
            Lex->sphead->m_parser_data.set_parameter_start_ptr(@5.cpp.end);
          }
          sp_pdparam_list       /*$7*/
          ')'                   /*$8*/
          {                     /*$9*/
            THD *thd= YYTHD;
            LEX *lex= thd->lex;

            lex->sphead->m_parser_data.set_parameter_end_ptr(@8.cpp.start);
            memset(&lex->sp_chistics, 0, sizeof(st_sp_chistics));

            // Default language is SQL
            lex->sp_chistics.language = {"SQL",3};
          }
          sp_c_chistics         /*$10*/
          {                     /*$11*/
            THD *thd= YYTHD;
            LEX *lex= thd->lex;

            lex->sphead->m_chistics= &lex->sp_chistics;
            lex->sphead->set_body_start(thd, yylloc.cpp.start);
          }
          stored_routine_body   /*$12*/
          {                     /*$13*/
            LEX *lex= Lex;
            lex->sql_command= SQLCOM_CREATE_PROCEDURE;
          }
        ;
