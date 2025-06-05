%start start_entry

%parse-param { class THD *YYTHD }
%parse-param { class Parse_tree_root **parse_tree }

%lex-param { class THD *YYTHD }
%define api.pure
%define api.prefix {my_sql_parser_}

%expect 63

%left KEYWORD_USED_AS_IDENT
%nonassoc TEXT_STRING
%left KEYWORD_USED_AS_KEYWORD
%right UNIQUE_SYM KEY_SYM
%left UNION_SYM EXCEPT_SYM
%left INTERSECT_SYM
%left CONDITIONLESS_JOIN
%left   JOIN_SYM INNER_SYM CROSS STRAIGHT_JOIN NATURAL LEFT RIGHT ON_SYM USING
%left   SET_VAR
%left   OR_SYM OR2_SYM
%left   XOR
%left   AND_SYM AND_AND_SYM
%left   BETWEEN_SYM CASE_SYM WHEN_SYM THEN_SYM ELSE
%left   EQ EQUAL_SYM GE GT_SYM LE LT NE IS LIKE REGEXP IN_SYM
%left   '|'
%left   '&'
%left   SHIFT_LEFT SHIFT_RIGHT
%left   '-' '+'
%left   '*' '/' '%' DIV_SYM MOD_SYM
%left   '^'
%left   OR_OR_SYM
%left   NEG '~'
%right  NOT_SYM NOT2_SYM
%right  BINARY_SYM COLLATE_SYM
%left  INTERVAL_SYM
%left SUBQUERY_AS_EXPR
%left '(' ')'

%left EMPTY_FROM_CLAUSE
%right INTO

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

deallocate:
          deallocate_or_drop PREPARE_SYM ident
          {
            THD *thd= YYTHD;
            LEX *lex= thd->lex;
            lex->sql_command= SQLCOM_DEALLOCATE_PREPARE;
            lex->prepared_stmt_name= to_lex_cstring($3);
          }
        ;

deallocate_or_drop:
          DEALLOCATE_SYM
        | DROP
        ;

prepare:
          PREPARE_SYM ident FROM prepare_src
          {
            THD *thd= YYTHD;
            LEX *lex= thd->lex;
            lex->sql_command= SQLCOM_PREPARE;
            lex->prepared_stmt_name= to_lex_cstring($2);
            /*
              We don't know know at this time whether there's a password
              in prepare_src, so we err on the side of caution.  Setting
              the flag will force a rewrite which will obscure all of
              prepare_src in the "Query" log line.  We'll see the actual
              query (with just the passwords obscured, if any) immediately
              afterwards in the "Prepare" log lines anyway, and then again
              in the "Execute" log line if and when prepare_src is executed.
            */
            lex->contains_plaintext_password= true;
          }
        ;

prepare_src:
          TEXT_STRING_sys
          {
            THD *thd= YYTHD;
            LEX *lex= thd->lex;
            lex->prepared_stmt_code= $1;
            lex->prepared_stmt_code_is_varref= false;
          }
        | '@' ident_or_text
          {
            THD *thd= YYTHD;
            LEX *lex= thd->lex;
            lex->prepared_stmt_code= $2;
            lex->prepared_stmt_code_is_varref= true;
          }
        ;

execute:
          EXECUTE_SYM ident
          {
            THD *thd= YYTHD;
            LEX *lex= thd->lex;
            lex->sql_command= SQLCOM_EXECUTE;
            lex->prepared_stmt_name= to_lex_cstring($2);
          }
          execute_using
          {}
        ;

execute_using:
          %empty
        | USING execute_var_list
        ;

execute_var_list:
          execute_var_list ',' execute_var_ident
        | execute_var_ident
        ;

execute_var_ident:
          '@' ident_or_text
          {
            LEX *lex=Lex;
            LEX_STRING *lexstr= (LEX_STRING*)sql_memdup(&$2, sizeof(LEX_STRING));
            if (!lexstr || lex->prepared_stmt_params.push_back(lexstr))
              MYSQL_YYABORT;
          }
        ;

/* help */

help:
          HELP_SYM
          {
            if (Lex->sphead)
            {
              my_error(ER_SP_BADSTATEMENT, MYF(0), "HELP");
              MYSQL_YYABORT;
            }
          }
          ident_or_text
          {
            LEX *lex= Lex;
            lex->sql_command= SQLCOM_HELP;
            lex->help_arg= $3.str;
          }
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

opt_channel:
          %empty { $$ = {}; }
        | FOR_SYM CHANNEL_SYM TEXT_STRING_sys_nonewline
          { $$ = to_lex_cstring($3); }
        ;

create_table_stmt:
          CREATE opt_temporary TABLE_SYM opt_if_not_exists table_ident
          '(' table_element_list ')' opt_create_table_options_etc
          {
            $$= NEW_PTN PT_create_table_stmt(@$, YYMEM_ROOT, $2, $4, $5,
                                             $7,
                                             $9.opt_create_table_options,
                                             $9.opt_partitioning,
                                             $9.on_duplicate,
                                             $9.opt_query_expression);
          }
        | CREATE opt_temporary TABLE_SYM opt_if_not_exists table_ident
          opt_create_table_options_etc
          {
            $$= NEW_PTN PT_create_table_stmt(@$, YYMEM_ROOT, $2, $4, $5,
                                             nullptr,
                                             $6.opt_create_table_options,
                                             $6.opt_partitioning,
                                             $6.on_duplicate,
                                             $6.opt_query_expression);
          }
        | CREATE opt_temporary TABLE_SYM opt_if_not_exists table_ident
          LIKE table_ident
          {
            $$= NEW_PTN PT_create_table_stmt(@$, YYMEM_ROOT, $2, $4, $5, $7);
          }
        | CREATE opt_temporary TABLE_SYM opt_if_not_exists table_ident
          '(' LIKE table_ident ')'
          {
            $$= NEW_PTN PT_create_table_stmt(@$, YYMEM_ROOT, $2, $4, $5, $8);
          }
        ;

create_role_stmt:
          CREATE ROLE_SYM opt_if_not_exists role_list
          {
            $$= NEW_PTN PT_create_role(@$, !!$3, $4);
          }
        ;

create_resource_group_stmt:
          CREATE RESOURCE_SYM GROUP_SYM ident TYPE_SYM
          opt_equal resource_group_types
          opt_resource_group_vcpu_list opt_resource_group_priority
          opt_resource_group_enable_disable
          {
            $$= NEW_PTN PT_create_resource_group(@$, to_lex_cstring($4), $7, $8, $9,
                                                 $10.is_default ? true :
                                                 $10.value);
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

create_index_stmt:
          CREATE opt_unique INDEX_SYM ident opt_index_type_clause
          ON_SYM table_ident '(' key_list_with_expression ')' opt_index_options
          opt_index_lock_and_algorithm
          {
            $$= NEW_PTN PT_create_index_stmt(@$, YYMEM_ROOT, $2, $4, $5,
                                             $7, $9, $11,
                                             $12.algo.get_or_default(),
                                             $12.lock.get_or_default());
          }
        | CREATE FULLTEXT_SYM INDEX_SYM ident ON_SYM table_ident
          '(' key_list_with_expression ')' opt_fulltext_index_options opt_index_lock_and_algorithm
          {
            $$= NEW_PTN PT_create_index_stmt(@$, YYMEM_ROOT, KEYTYPE_FULLTEXT, $4,
                                             nullptr, $6, $8, $10,
                                             $11.algo.get_or_default(),
                                             $11.lock.get_or_default());
          }
        | CREATE SPATIAL_SYM INDEX_SYM ident ON_SYM table_ident
          '(' key_list_with_expression ')' opt_spatial_index_options opt_index_lock_and_algorithm
          {
            $$= NEW_PTN PT_create_index_stmt(@$, YYMEM_ROOT, KEYTYPE_SPATIAL, $4,
                                             nullptr, $6, $8, $10,
                                             $11.algo.get_or_default(),
                                             $11.lock.get_or_default());
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

ev_schedule_time:
          EVERY_SYM expr interval
          {
            ITEMIZE($2, &$2);

            Lex->event_parse_data->item_expression= $2;
            Lex->event_parse_data->interval= $3;
          }
          ev_starts
          ev_ends
        | AT_SYM expr
          {
            ITEMIZE($2, &$2);

            Lex->event_parse_data->item_execute_at= $2;
          }
        ;

opt_ev_status:
          %empty { $$= 0; }
        | ENABLE_SYM
          {
            Lex->event_parse_data->status= Event_parse_data::ENABLED;
            Lex->event_parse_data->status_changed= true;
            $$= 1;
          }
        | DISABLE_SYM ON_SYM SLAVE
          {
            push_deprecated_warn(YYTHD, "<CREATE|ALTER> EVENT ... DISABLE ON SLAVE",
                                        "<CREATE|ALTER> EVENT ... DISABLE ON REPLICA");
            Lex->event_parse_data->status= Event_parse_data::REPLICA_SIDE_DISABLED;
            Lex->event_parse_data->status_changed= true;
            $$= 1;
          }
        | DISABLE_SYM ON_SYM REPLICA_SYM
          {
            Lex->event_parse_data->status= Event_parse_data::REPLICA_SIDE_DISABLED;
            Lex->event_parse_data->status_changed= true;
            $$= 1;
          }
        | DISABLE_SYM
          {
            Lex->event_parse_data->status= Event_parse_data::DISABLED;
            Lex->event_parse_data->status_changed= true;
            $$= 1;
          }
        ;

ev_starts:
          %empty
          {
            Item *item= NEW_PTN Item_func_now_local(0);
            if (item == nullptr)
              MYSQL_YYABORT;
            Lex->event_parse_data->item_starts= item;
          }
        | STARTS_SYM expr
          {
            ITEMIZE($2, &$2);

            Lex->event_parse_data->item_starts= $2;
          }
        ;

ev_ends:
          %empty
        | ENDS_SYM expr
          {
            ITEMIZE($2, &$2);

            Lex->event_parse_data->item_ends= $2;
          }
        ;

opt_ev_on_completion:
          %empty { $$= 0; }
        | ev_on_completion
        ;

ev_on_completion:
          ON_SYM COMPLETION_SYM PRESERVE_SYM
          {
            Lex->event_parse_data->on_completion=
                                  Event_parse_data::ON_COMPLETION_PRESERVE;
            $$= 1;
          }
        | ON_SYM COMPLETION_SYM NOT_SYM PRESERVE_SYM
          {
            Lex->event_parse_data->on_completion=
                                  Event_parse_data::ON_COMPLETION_DROP;
            $$= 1;
          }
        ;

opt_ev_comment:
          %empty { $$= 0; }
        | COMMENT_SYM TEXT_STRING_sys
          {
            Lex->event_parse_data->comment= $2;
            $$= 1;
          }
        ;

ev_sql_stmt:
          {
            THD *thd= YYTHD;
            LEX *lex= thd->lex;

            /*
              This stops the following :
              - CREATE EVENT ... DO CREATE EVENT ...;
              - ALTER  EVENT ... DO CREATE EVENT ...;
              - CREATE EVENT ... DO ALTER EVENT DO ....;
              - CREATE PROCEDURE ... BEGIN CREATE EVENT ... END|
              This allows:
              - CREATE EVENT ... DO DROP EVENT yyy;
              - CREATE EVENT ... DO ALTER EVENT yyy;
                (the nested ALTER EVENT can have anything but DO clause)
              - ALTER  EVENT ... DO ALTER EVENT yyy;
                (the nested ALTER EVENT can have anything but DO clause)
              - ALTER  EVENT ... DO DROP EVENT yyy;
              - CREATE PROCEDURE ... BEGIN ALTER EVENT ... END|
                (the nested ALTER EVENT can have anything but DO clause)
              - CREATE PROCEDURE ... BEGIN DROP EVENT ... END|
            */
            if (lex->sphead)
            {
              my_error(ER_EVENT_RECURSION_FORBIDDEN, MYF(0));
              MYSQL_YYABORT;
            }

            sp_head *sp= sp_start_parsing(thd,
                                          enum_sp_type::EVENT,
                                          lex->event_parse_data->identifier);

            if (!sp)
              MYSQL_YYABORT;

            lex->sphead= sp;

            memset(&lex->sp_chistics, 0, sizeof(st_sp_chistics));
            sp->m_chistics= &lex->sp_chistics;

            // Default language is SQL
            lex->sp_chistics.language = {"SQL",3};

            /*
              Set a body start to the end of the last preprocessed token
              before ev_sql_stmt:
            */
            sp->set_body_start(thd, @0.cpp.end);
          }
          ev_sql_stmt_inner
          {
            THD *thd= YYTHD;
            LEX *lex= thd->lex;

            sp_finish_parsing(thd);

            lex->sp_chistics.suid= SP_IS_SUID;  //always the definer!
            lex->event_parse_data->body_changed= true;
          }
        ;

ev_sql_stmt_inner:
          sp_proc_stmt_statement
        | sp_proc_stmt_return
        | sp_proc_stmt_if
        | case_stmt_specification
        | sp_labeled_block
        | sp_unlabeled_block
        | sp_labeled_control
        | sp_proc_stmt_unlabeled
        | sp_proc_stmt_leave
        | sp_proc_stmt_iterate
        | sp_proc_stmt_open
        | sp_proc_stmt_fetch
        | sp_proc_stmt_close
        ;

sp_name:
          ident '.' ident
          {
            if (!$1.str ||
                (check_and_convert_db_name(&$1, false) != Ident_name_check::OK))
              MYSQL_YYABORT;
            if (sp_check_name(&$3))
            {
              MYSQL_YYABORT;
            }
            $$= new (YYMEM_ROOT) sp_name(to_lex_cstring($1), $3, true);
            if ($$ == nullptr)
              MYSQL_YYABORT;
            $$->init_qname(YYTHD);
          }
        | ident
          {
            THD *thd= YYTHD;
            LEX *lex= thd->lex;
            LEX_CSTRING db;
            if (sp_check_name(&$1))
            {
              MYSQL_YYABORT;
            }
            if (lex->copy_db_to(&db.str, &db.length))
              MYSQL_YYABORT;
            $$= new (YYMEM_ROOT) sp_name(db, $1, false);
            if ($$ == nullptr)
              MYSQL_YYABORT;
            $$->init_qname(thd);
          }
        ;

sp_a_chistics:
          %empty {}
        | sp_a_chistics sp_chistic {}
        ;

sp_c_chistics:
          %empty {}
        | sp_c_chistics sp_c_chistic {}
        ;

/* Characteristics for both create and alter */
sp_chistic:
          COMMENT_SYM TEXT_STRING_sys
          { Lex->sp_chistics.comment= to_lex_cstring($2); }
        | LANGUAGE_SYM SQL_SYM
          { Lex->sp_chistics.language= {"SQL",3}; }
        | LANGUAGE_SYM ident
          { Lex->sp_chistics.language= to_lex_cstring($2); }
        | NO_SYM SQL_SYM
          { Lex->sp_chistics.daccess= SP_NO_SQL; }
        | CONTAINS_SYM SQL_SYM
          { Lex->sp_chistics.daccess= SP_CONTAINS_SQL; }
        | READS_SYM SQL_SYM DATA_SYM
          { Lex->sp_chistics.daccess= SP_READS_SQL_DATA; }
        | MODIFIES_SYM SQL_SYM DATA_SYM
          { Lex->sp_chistics.daccess= SP_MODIFIES_SQL_DATA; }
        | sp_suid
          {}
        ;

/* Create characteristics */
sp_c_chistic:
          sp_chistic            { }
        | DETERMINISTIC_SYM     { Lex->sp_chistics.detistic= true; }
        | not DETERMINISTIC_SYM { Lex->sp_chistics.detistic= false; }
        ;

sp_suid:
          SQL_SYM SECURITY_SYM DEFINER_SYM
          {
            Lex->sp_chistics.suid= SP_IS_SUID;
          }
        | SQL_SYM SECURITY_SYM INVOKER_SYM
          {
            Lex->sp_chistics.suid= SP_IS_NOT_SUID;
          }
        ;

call_stmt:
          CALL_SYM sp_name opt_paren_expr_list
          {
            $$= NEW_PTN PT_call(@$, $2, $3);
          }
        ;

opt_paren_expr_list:
            %empty { $$= nullptr; }
          | '(' opt_expr_list ')'
            {
              $$= $2;
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

sp_proc_stmts:
          %empty {}
        | sp_proc_stmts  sp_proc_stmt ';'
        ;

sp_proc_stmts1:
          sp_proc_stmt ';' {}
        | sp_proc_stmts1  sp_proc_stmt ';'
        ;

sp_decls:
          %empty
          {
            $$.vars= $$.conds= $$.hndlrs= $$.curs= 0;
          }
        | sp_decls sp_decl ';'
          {
            /* We check for declarations out of (standard) order this way
              because letting the grammar rules reflect it caused tricky
               shift/reduce conflicts with the wrong result. (And we get
               better error handling this way.) */
            if (($2.vars || $2.conds) && ($1.curs || $1.hndlrs))
            { /* Variable or condition following cursor or handler */
              my_error(ER_SP_VARCOND_AFTER_CURSHNDLR, MYF(0));
              MYSQL_YYABORT;
            }
            if ($2.curs && $1.hndlrs)
            { /* Cursor following handler */
              my_error(ER_SP_CURSOR_AFTER_HANDLER, MYF(0));
              MYSQL_YYABORT;
            }
            $$.vars= $1.vars + $2.vars;
            $$.conds= $1.conds + $2.conds;
            $$.hndlrs= $1.hndlrs + $2.hndlrs;
            $$.curs= $1.curs + $2.curs;
          }
        ;

sp_decl:
          DECLARE_SYM           /*$1*/
          sp_decl_idents        /*$2*/
          type                  /*$3*/
          opt_collate           /*$4*/
          sp_opt_default        /*$5*/
          {                     /*$6*/
            THD *thd= YYTHD;
            LEX *lex= thd->lex;
            sp_head *sp= lex->sphead;
            sp_pcontext *pctx= lex->get_sp_current_parsing_ctx();

            sp->reset_lex(thd);
            lex= thd->lex;

            pctx->declare_var_boundary($2);

            CONTEXTUALIZE($3);
            enum enum_field_types var_type= $3->type;
            const CHARSET_INFO *cs= $3->get_charset();
            if (merge_sp_var_charset_and_collation(cs, $4, &cs))
              MYSQL_YYABORT;

            uint num_vars= pctx->context_var_count();
            Item *dflt_value_item= $5.expr;

            LEX_CSTRING dflt_value_query= EMPTY_CSTR;

            if (dflt_value_item)
            {
              ITEMIZE(dflt_value_item, &dflt_value_item);
              const char *expr_start_ptr= $5.expr_start;
              if (lex->is_metadata_used())
              {
                dflt_value_query= make_string(thd, expr_start_ptr,
                                              @5.raw.end);
                if (!dflt_value_query.str)
                  MYSQL_YYABORT;
              }
            }
            else
            {
              dflt_value_item= NEW_PTN Item_null();

              if (dflt_value_item == nullptr)
                MYSQL_YYABORT;
            }

            // We can have several variables in DECLARE statement.
            // We need to create an sp_instr_set instruction for each variable.

            for (uint i = num_vars-$2 ; i < num_vars ; i++)
            {
              uint var_idx= pctx->var_context2runtime(i);
              sp_variable *spvar= pctx->find_variable(var_idx);

              if (!spvar)
                MYSQL_YYABORT;

              spvar->type= var_type;
              spvar->default_value= dflt_value_item;

              if (spvar->field_def.init(thd, "", var_type,
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

              if (prepare_sp_create_field(thd, &spvar->field_def))
                MYSQL_YYABORT;

              spvar->field_def.field_name= spvar->name.str;
              spvar->field_def.is_nullable= true;

              /* The last instruction is responsible for freeing LEX. */

              sp_instr_set *is= NEW_PTN sp_instr_set(sp->instructions(),
                                                     lex,
                                                     var_idx,
                                                     dflt_value_item,
                                                     dflt_value_query,
                                                     (i == num_vars - 1));

              if (!is || sp->add_instr(thd, is))
                MYSQL_YYABORT;
            }

            pctx->declare_var_boundary(0);
            if (sp->restore_lex(thd))
              MYSQL_YYABORT;
            $$.vars= $2;
            $$.conds= $$.hndlrs= $$.curs= 0;
          }
        | DECLARE_SYM ident CONDITION_SYM FOR_SYM sp_cond
          {
            THD *thd= YYTHD;
            LEX *lex= thd->lex;
            sp_pcontext *pctx= lex->get_sp_current_parsing_ctx();

            if (pctx->find_condition($2, true))
            {
              my_error(ER_SP_DUP_COND, MYF(0), $2.str);
              MYSQL_YYABORT;
            }
            if(pctx->add_condition(thd, $2, $5))
              MYSQL_YYABORT;
            lex->keep_diagnostics= DA_KEEP_DIAGNOSTICS; // DECLARE COND FOR
            $$.vars= $$.hndlrs= $$.curs= 0;
            $$.conds= 1;
          }
        | DECLARE_SYM sp_handler_type HANDLER_SYM FOR_SYM
          {
            THD *thd= YYTHD;
            LEX *lex= thd->lex;
            sp_head *sp= lex->sphead;

            sp_pcontext *parent_pctx= lex->get_sp_current_parsing_ctx();

            sp_pcontext *handler_pctx=
              parent_pctx->push_context(thd, sp_pcontext::HANDLER_SCOPE);

            sp_handler *h=
              parent_pctx->add_handler(thd, (sp_handler::enum_type) $2);

            lex->set_sp_current_parsing_ctx(handler_pctx);

            sp_instr_hpush_jump *i=
              NEW_PTN sp_instr_hpush_jump(sp->instructions(), handler_pctx, h);

            if (!i || sp->add_instr(thd, i))
              MYSQL_YYABORT;

            if ($2 == sp_handler::CONTINUE)
            {
              // Mark the end of CONTINUE handler scope.

              if (sp->m_parser_data.add_backpatch_entry(
                    i, handler_pctx->last_label()))
              {
                MYSQL_YYABORT;
              }
            }

            if (sp->m_parser_data.add_backpatch_entry(
                  i, handler_pctx->push_label(thd, EMPTY_CSTR, 0)))
            {
              MYSQL_YYABORT;
            }

            lex->keep_diagnostics= DA_KEEP_DIAGNOSTICS; // DECL HANDLER FOR
          }
          sp_hcond_list sp_proc_stmt
          {
            THD *thd= YYTHD;
            LEX *lex= Lex;
            sp_head *sp= lex->sphead;
            sp_pcontext *pctx= lex->get_sp_current_parsing_ctx();
            sp_label *hlab= pctx->pop_label(); /* After this hdlr */

            if ($2 == sp_handler::CONTINUE)
            {
              sp_instr_hreturn *i=
                NEW_PTN sp_instr_hreturn(sp->instructions(), pctx);

              if (!i || sp->add_instr(thd, i))
                MYSQL_YYABORT;
            }
            else
            {  /* EXIT or UNDO handler, just jump to the end of the block */
              sp_instr_hreturn *i=
                NEW_PTN sp_instr_hreturn(sp->instructions(), pctx);

              if (i == nullptr ||
                  sp->add_instr(thd, i) ||
                  sp->m_parser_data.add_backpatch_entry(i, pctx->last_label()))
                MYSQL_YYABORT;
            }

            sp->m_parser_data.do_backpatch(hlab, sp->instructions());

            lex->set_sp_current_parsing_ctx(pctx->pop_context());

            $$.vars= $$.conds= $$.curs= 0;
            $$.hndlrs= 1;
          }
        | DECLARE_SYM   /*$1*/
          ident         /*$2*/
          CURSOR_SYM    /*$3*/
          FOR_SYM       /*$4*/
          {             /*$5*/
            THD *thd= YYTHD;
            LEX *lex= Lex;
            sp_head *sp= lex->sphead;

            sp->reset_lex(thd);
            sp->m_parser_data.set_current_stmt_start_ptr(@4.raw.end);
          }
          select_stmt   /*$6*/
          {             /*$7*/
            MAKE_CMD($6);

            THD *thd= YYTHD;
            LEX *cursor_lex= Lex;
            sp_head *sp= cursor_lex->sphead;

            assert(cursor_lex->sql_command == SQLCOM_SELECT);

            if (cursor_lex->result)
            {
              my_error(ER_SP_BAD_CURSOR_SELECT, MYF(0));
              MYSQL_YYABORT;
            }

            cursor_lex->m_sql_cmd->set_as_part_of_sp();
            cursor_lex->sp_lex_in_use= true;

            if (sp->restore_lex(thd))
              MYSQL_YYABORT;

            LEX *lex= Lex;
            sp_pcontext *pctx= lex->get_sp_current_parsing_ctx();

            uint offp;

            if (pctx->find_cursor($2, &offp, true))
            {
              my_error(ER_SP_DUP_CURS, MYF(0), $2.str);
              delete cursor_lex;
              MYSQL_YYABORT;
            }

            LEX_CSTRING cursor_query= EMPTY_CSTR;

            if (cursor_lex->is_metadata_used())
            {
              cursor_query=
                make_string(thd,
                            sp->m_parser_data.get_current_stmt_start_ptr(),
                            @6.raw.end);

              if (!cursor_query.str)
                MYSQL_YYABORT;
            }

            sp_instr_cpush *i=
              NEW_PTN sp_instr_cpush(sp->instructions(), pctx,
                                     cursor_lex, cursor_query,
                                     pctx->current_cursor_count());

            if (i == nullptr ||
                sp->add_instr(thd, i) ||
                pctx->add_cursor($2))
            {
              MYSQL_YYABORT;
            }

            $$.vars= $$.conds= $$.hndlrs= 0;
            $$.curs= 1;
          }
        ;

sp_handler_type:
          EXIT_SYM      { $$= sp_handler::EXIT; }
        | CONTINUE_SYM  { $$= sp_handler::CONTINUE; }
        /*| UNDO_SYM      { QQ No yet } */
        ;

sp_hcond_list:
          sp_hcond_element
          { $$= 1; }
        | sp_hcond_list ',' sp_hcond_element
          { $$+= 1; }
        ;

sp_hcond_element:
          sp_hcond
          {
            LEX *lex= Lex;
            sp_head *sp= lex->sphead;
            sp_pcontext *pctx= lex->get_sp_current_parsing_ctx();
            sp_pcontext *parent_pctx= pctx->parent_context();

            if (parent_pctx->check_duplicate_handler($1))
            {
              my_error(ER_SP_DUP_HANDLER, MYF(0));
              MYSQL_YYABORT;
            }
            else
            {
              sp_instr_hpush_jump *i=
                (sp_instr_hpush_jump *)sp->last_instruction();

              i->add_condition($1);
            }
          }
        ;

sp_cond:
          ulong_num
          { /* mysql errno */
            if ($1 == 0)
            {
              my_error(ER_WRONG_VALUE, MYF(0), "CONDITION", "0");
              MYSQL_YYABORT;
            }
            $$= NEW_PTN sp_condition_value($1);
            if ($$ == nullptr)
              MYSQL_YYABORT;
          }
        | sqlstate
        ;

sqlstate:
          SQLSTATE_SYM opt_value TEXT_STRING_literal
          { /* SQLSTATE */

            /*
              An error is triggered:
                - if the specified string is not a valid SQLSTATE,
                - or if it represents the completion condition -- it is not
                  allowed to SIGNAL, or declare a handler for the completion
                  condition.
            */
            if (!is_sqlstate_valid(&$3) || is_sqlstate_completion($3.str))
            {
              my_error(ER_SP_BAD_SQLSTATE, MYF(0), $3.str);
              MYSQL_YYABORT;
            }
            $$= NEW_PTN sp_condition_value($3.str);
            if ($$ == nullptr)
              MYSQL_YYABORT;
          }
        ;

opt_value:
          %empty {}
        | VALUE_SYM    {}
        ;

sp_hcond:
          sp_cond
          {
            $$= $1;
          }
        | ident /* CONDITION name */
          {
            LEX *lex= Lex;
            sp_pcontext *pctx= lex->get_sp_current_parsing_ctx();

            $$= pctx->find_condition($1, false);

            if ($$ == nullptr)
            {
              my_error(ER_SP_COND_MISMATCH, MYF(0), $1.str);
              MYSQL_YYABORT;
            }
          }
        | SQLWARNING_SYM /* SQLSTATEs 01??? */
          {
            $$= NEW_PTN sp_condition_value(sp_condition_value::WARNING);
            if ($$ == nullptr)
              MYSQL_YYABORT;
          }
        | not FOUND_SYM /* SQLSTATEs 02??? */
          {
            $$= NEW_PTN sp_condition_value(sp_condition_value::NOT_FOUND);
            if ($$ == nullptr)
              MYSQL_YYABORT;
          }
        | SQLEXCEPTION_SYM /* All other SQLSTATEs */
          {
            $$= NEW_PTN sp_condition_value(sp_condition_value::EXCEPTION);
            if ($$ == nullptr)
              MYSQL_YYABORT;
          }
        ;

signal_stmt:
          SIGNAL_SYM signal_value opt_set_signal_information
          {
            THD *thd= YYTHD;
            LEX *lex= thd->lex;

            lex->sql_command= SQLCOM_SIGNAL;
            lex->m_sql_cmd= NEW_PTN Sql_cmd_signal($2, $3);
            if (lex->m_sql_cmd == nullptr)
              MYSQL_YYABORT;
          }
        ;

signal_value:
          ident
          {
            LEX *lex= Lex;
            sp_pcontext *pctx= lex->get_sp_current_parsing_ctx();

            if (!pctx)
            {
              /* SIGNAL foo cannot be used outside of stored programs */
              my_error(ER_SP_COND_MISMATCH, MYF(0), $1.str);
              MYSQL_YYABORT;
            }

            sp_condition_value *cond= pctx->find_condition($1, false);

            if (!cond)
            {
              my_error(ER_SP_COND_MISMATCH, MYF(0), $1.str);
              MYSQL_YYABORT;
            }
            if (cond->type != sp_condition_value::SQLSTATE)
            {
              my_error(ER_SIGNAL_BAD_CONDITION_TYPE, MYF(0));
              MYSQL_YYABORT;
            }
            $$= cond;
          }
        | sqlstate
          { $$= $1; }
        ;

opt_signal_value:
          %empty { $$= nullptr; }
        | signal_value
          { $$= $1; }
        ;

opt_set_signal_information:
          %empty { $$= NEW_PTN Set_signal_information(); }
        | SET_SYM signal_information_item_list
          { $$= $2; }
        ;

signal_information_item_list:
          signal_condition_information_item_name EQ signal_allowed_expr
          {
            $$= NEW_PTN Set_signal_information();
            if ($$->set_item($1, $3))
              MYSQL_YYABORT;
          }
        | signal_information_item_list ','
          signal_condition_information_item_name EQ signal_allowed_expr
          {
            $$= $1;
            if ($$->set_item($3, $5))
              MYSQL_YYABORT;
          }
        ;

/*
  Only a limited subset of <expr> are allowed in SIGNAL/RESIGNAL.
*/
signal_allowed_expr:
          literal_or_null
          { ITEMIZE($1, &$$); }
        | rvalue_system_or_user_variable
          { ITEMIZE($1, &$$); }
        | simple_ident
          { ITEMIZE($1, &$$); }
        ;

/* conditions that can be set in signal / resignal */
signal_condition_information_item_name:
          CLASS_ORIGIN_SYM
          { $$= CIN_CLASS_ORIGIN; }
        | SUBCLASS_ORIGIN_SYM
          { $$= CIN_SUBCLASS_ORIGIN; }
        | CONSTRAINT_CATALOG_SYM
          { $$= CIN_CONSTRAINT_CATALOG; }
        | CONSTRAINT_SCHEMA_SYM
          { $$= CIN_CONSTRAINT_SCHEMA; }
        | CONSTRAINT_NAME_SYM
          { $$= CIN_CONSTRAINT_NAME; }
        | CATALOG_NAME_SYM
          { $$= CIN_CATALOG_NAME; }
        | SCHEMA_NAME_SYM
          { $$= CIN_SCHEMA_NAME; }
        | TABLE_NAME_SYM
          { $$= CIN_TABLE_NAME; }
        | COLUMN_NAME_SYM
          { $$= CIN_COLUMN_NAME; }
        | CURSOR_NAME_SYM
          { $$= CIN_CURSOR_NAME; }
        | MESSAGE_TEXT_SYM
          { $$= CIN_MESSAGE_TEXT; }
        | MYSQL_ERRNO_SYM
          { $$= CIN_MYSQL_ERRNO; }
        ;

resignal_stmt:
          RESIGNAL_SYM opt_signal_value opt_set_signal_information
          {
            THD *thd= YYTHD;
            LEX *lex= thd->lex;

            lex->sql_command= SQLCOM_RESIGNAL;
            lex->keep_diagnostics= DA_KEEP_DIAGNOSTICS; // RESIGNAL doesn't clear diagnostics
            lex->m_sql_cmd= NEW_PTN Sql_cmd_resignal($2, $3);
            if (lex->m_sql_cmd == nullptr)
              MYSQL_YYABORT;
          }
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

/*
   Only a limited subset of <expr> are allowed in GET DIAGNOSTICS
   <condition number>, same subset as for SIGNAL/RESIGNAL.
*/
condition_number:
          signal_allowed_expr
          { $$= $1; }
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

sp_decl_idents:
          ident
          {
            /* NOTE: field definition is filled in sp_decl section. */

            THD *thd= YYTHD;
            LEX *lex= thd->lex;
            sp_pcontext *pctx= lex->get_sp_current_parsing_ctx();

            if (pctx->find_variable($1.str, $1.length, true))
            {
              my_error(ER_SP_DUP_VAR, MYF(0), $1.str);
              MYSQL_YYABORT;
            }

            pctx->add_variable(thd,
                               $1,
                               MYSQL_TYPE_DECIMAL,
                               sp_variable::MODE_IN);
            $$= 1;
          }
        | sp_decl_idents ',' ident
          {
            /* NOTE: field definition is filled in sp_decl section. */

            THD *thd= YYTHD;
            LEX *lex= thd->lex;
            sp_pcontext *pctx= lex->get_sp_current_parsing_ctx();

            if (pctx->find_variable($3.str, $3.length, true))
            {
              my_error(ER_SP_DUP_VAR, MYF(0), $3.str);
              MYSQL_YYABORT;
            }

            pctx->add_variable(thd,
                               $3,
                               MYSQL_TYPE_DECIMAL,
                               sp_variable::MODE_IN);
            $$= $1 + 1;
          }
        ;

sp_opt_default:
          %empty
          {
            $$.expr_start= nullptr;
            $$.expr = nullptr;
          }
        | DEFAULT_SYM expr
          {
            $$.expr_start= @1.raw.end;
            $$.expr= $2;
          }
        ;

sp_proc_stmt:
          sp_proc_stmt_statement
        | sp_proc_stmt_return
        | sp_proc_stmt_if
        | case_stmt_specification
        | sp_labeled_block
        | sp_unlabeled_block
        | sp_labeled_control
        | sp_proc_stmt_unlabeled
        | sp_proc_stmt_leave
        | sp_proc_stmt_iterate
        | sp_proc_stmt_open
        | sp_proc_stmt_fetch
        | sp_proc_stmt_close
        ;

sp_proc_stmt_if:
          IF
          { Lex->sphead->m_parser_data.new_cont_backpatch(); }
          sp_if END IF
          {
            sp_head *sp= Lex->sphead;

            sp->m_parser_data.do_cont_backpatch(sp->instructions());
          }
        ;

sp_proc_stmt_statement:
          {
            THD *thd= YYTHD;
            LEX *lex= thd->lex;
            sp_head *sp= lex->sphead;

            sp->reset_lex(thd);
            sp->m_parser_data.set_current_stmt_start_ptr(yylloc.raw.start);
          }
          simple_statement
          {
            if ($2 != nullptr)
              MAKE_CMD($2);

            THD *thd= YYTHD;
            LEX *lex= thd->lex;
            sp_head *sp= lex->sphead;

            sp->m_flags|= sp_get_flags_for_command(lex);
            if (lex->sql_command == SQLCOM_CHANGE_DB)
            { /* "USE db" doesn't work in a procedure */
              my_error(ER_SP_BADSTATEMENT, MYF(0), "USE");
              MYSQL_YYABORT;
            }

            // Mark statement as belonging to a stored procedure:
            if (lex->m_sql_cmd != nullptr)
              lex->m_sql_cmd->set_as_part_of_sp();

            /*
              Don't add an instruction for SET statements, since all
              instructions for them were already added during processing
              of "set" rule.
            */
            assert((lex->sql_command != SQLCOM_SET_OPTION &&
                         lex->sql_command != SQLCOM_SET_PASSWORD) ||
                        lex->var_list.is_empty());
            if (lex->sql_command != SQLCOM_SET_OPTION &&
                lex->sql_command != SQLCOM_SET_PASSWORD)
            {
              /* Extract the query statement from the tokenizer. */

              LEX_CSTRING query=
                make_string(thd,
                            sp->m_parser_data.get_current_stmt_start_ptr(),
                            @2.raw.end);

              if (!query.str)
                MYSQL_YYABORT;

              /* Add instruction. */

              sp_instr_stmt *i=
                NEW_PTN sp_instr_stmt(sp->instructions(), lex, query);

              if (!i || sp->add_instr(thd, i))
                MYSQL_YYABORT;
            }

            if (sp->restore_lex(thd))
              MYSQL_YYABORT;
          }
        ;

sp_proc_stmt_return:
          RETURN_SYM    /*$1*/
          {             /*$2*/
            THD *thd= YYTHD;
            LEX *lex= thd->lex;
            sp_head *sp= lex->sphead;

            sp->reset_lex(thd);
          }
          expr          /*$3*/
          {             /*$4*/
            ITEMIZE($3, &$3);

            THD *thd= YYTHD;
            LEX *lex= thd->lex;
            sp_head *sp= lex->sphead;

            /* Extract expression string. */

            LEX_CSTRING expr_query= EMPTY_CSTR;

            const char *expr_start_ptr= @1.raw.end;

            if (lex->is_metadata_used())
            {
              expr_query= make_string(thd, expr_start_ptr, @3.raw.end);
              if (!expr_query.str)
                MYSQL_YYABORT;
            }

            /* Check that this is a stored function. */

            if (sp->m_type != enum_sp_type::FUNCTION)
            {
              my_error(ER_SP_BADRETURN, MYF(0));
              MYSQL_YYABORT;
            }

            /* Indicate that we've reached RETURN statement. */

            sp->m_flags|= sp_head::HAS_RETURN;

            /* Add instruction. */

            sp_instr_freturn *i=
              NEW_PTN sp_instr_freturn(sp->instructions(), lex, $3, expr_query,
                                       sp->m_return_field_def.sql_type);

            if (i == nullptr ||
                sp->add_instr(thd, i) ||
                sp->restore_lex(thd))
            {
              MYSQL_YYABORT;
            }
          }
        ;

sp_proc_stmt_unlabeled:
          { /* Unlabeled controls get a secret label. */
            THD *thd= YYTHD;
            LEX *lex= thd->lex;
            sp_head *sp= lex->sphead;
            sp_pcontext *pctx= lex->get_sp_current_parsing_ctx();

            pctx->push_label(thd,
                             EMPTY_CSTR,
                             sp->instructions());
          }
          sp_unlabeled_control
          {
            LEX *lex= Lex;
            sp_head *sp= lex->sphead;
            sp_pcontext *pctx= lex->get_sp_current_parsing_ctx();

            sp->m_parser_data.do_backpatch(pctx->pop_label(),
                                           sp->instructions());
          }
        ;

sp_proc_stmt_leave:
          LEAVE_SYM label_ident
          {
            THD *thd= YYTHD;
            LEX *lex= Lex;
            sp_head *sp = lex->sphead;
            sp_pcontext *pctx= lex->get_sp_current_parsing_ctx();
            sp_label *lab= pctx->find_label($2);

            if (! lab)
            {
              my_error(ER_SP_LILABEL_MISMATCH, MYF(0), "LEAVE", $2.str);
              MYSQL_YYABORT;
            }

            uint ip= sp->instructions();

            /*
              When jumping to a BEGIN-END block end, the target jump
              points to the block hpop/cpop cleanup instructions,
              so we should exclude the block context here.
              When jumping to something else (i.e., sp_label::ITERATION),
              there are no hpop/cpop at the jump destination,
              so we should include the block context here for cleanup.
            */
            bool exclusive= (lab->type == sp_label::BEGIN);

            size_t n= pctx->diff_handlers(lab->ctx, exclusive);

            if (n)
            {
              sp_instr_hpop *hpop= NEW_PTN sp_instr_hpop(ip++, pctx);

              if (!hpop || sp->add_instr(thd, hpop))
                MYSQL_YYABORT;
            }

            n= pctx->diff_cursors(lab->ctx, exclusive);

            if (n)
            {
              sp_instr_cpop *cpop= NEW_PTN sp_instr_cpop(ip++, pctx, n);

              if (!cpop || sp->add_instr(thd, cpop))
                MYSQL_YYABORT;
            }

            sp_instr_jump *i= NEW_PTN sp_instr_jump(ip, pctx);

            if (!i ||
                /* Jumping forward */
                sp->m_parser_data.add_backpatch_entry(i, lab) ||
                sp->add_instr(thd, i))
              MYSQL_YYABORT;
          }
        ;

sp_proc_stmt_iterate:
          ITERATE_SYM label_ident
          {
            THD *thd= YYTHD;
            LEX *lex= Lex;
            sp_head *sp= lex->sphead;
            sp_pcontext *pctx= lex->get_sp_current_parsing_ctx();
            sp_label *lab= pctx->find_label($2);

            if (! lab || lab->type != sp_label::ITERATION)
            {
              my_error(ER_SP_LILABEL_MISMATCH, MYF(0), "ITERATE", $2.str);
              MYSQL_YYABORT;
            }

            uint ip= sp->instructions();

            /* Inclusive the dest. */
            size_t n= pctx->diff_handlers(lab->ctx, false);

            if (n)
            {
              sp_instr_hpop *hpop= NEW_PTN sp_instr_hpop(ip++, pctx);

              if (!hpop || sp->add_instr(thd, hpop))
                MYSQL_YYABORT;
            }

            /* Inclusive the dest. */
            n= pctx->diff_cursors(lab->ctx, false);

            if (n)
            {
              sp_instr_cpop *cpop= NEW_PTN sp_instr_cpop(ip++, pctx, n);

              if (!cpop || sp->add_instr(thd, cpop))
                MYSQL_YYABORT;
            }

            /* Jump back */
            sp_instr_jump *i= NEW_PTN sp_instr_jump(ip, pctx, lab->ip);

            if (!i || sp->add_instr(thd, i))
              MYSQL_YYABORT;
          }
        ;

sp_proc_stmt_open:
          OPEN_SYM ident
          {
            THD *thd= YYTHD;
            LEX *lex= Lex;
            sp_head *sp= lex->sphead;
            sp_pcontext *pctx= lex->get_sp_current_parsing_ctx();
            uint offset;

            if (! pctx->find_cursor($2, &offset, false))
            {
              my_error(ER_SP_CURSOR_MISMATCH, MYF(0), $2.str);
              MYSQL_YYABORT;
            }

            sp_instr_copen *i= NEW_PTN sp_instr_copen(sp->instructions(), pctx,
                                                      offset);

            if (!i || sp->add_instr(thd, i))
              MYSQL_YYABORT;
          }
        ;

sp_proc_stmt_fetch:
          FETCH_SYM sp_opt_fetch_noise ident INTO
          {
            THD *thd= YYTHD;
            LEX *lex= Lex;
            sp_head *sp= lex->sphead;
            sp_pcontext *pctx= lex->get_sp_current_parsing_ctx();
            uint offset;

            if (! pctx->find_cursor($3, &offset, false))
            {
              my_error(ER_SP_CURSOR_MISMATCH, MYF(0), $3.str);
              MYSQL_YYABORT;
            }

            sp_instr_cfetch *i= NEW_PTN sp_instr_cfetch(sp->instructions(),
                                                        pctx, offset);

            if (!i || sp->add_instr(thd, i))
              MYSQL_YYABORT;
          }
          sp_fetch_list
          {}
        ;

sp_proc_stmt_close:
          CLOSE_SYM ident
          {
            THD *thd= YYTHD;
            LEX *lex= Lex;
            sp_head *sp= lex->sphead;
            sp_pcontext *pctx= lex->get_sp_current_parsing_ctx();
            uint offset;

            if (! pctx->find_cursor($2, &offset, false))
            {
              my_error(ER_SP_CURSOR_MISMATCH, MYF(0), $2.str);
              MYSQL_YYABORT;
            }

            sp_instr_cclose *i=
              NEW_PTN sp_instr_cclose(sp->instructions(), pctx, offset);

            if (!i || sp->add_instr(thd, i))
              MYSQL_YYABORT;
          }
        ;

sp_opt_fetch_noise:
          %empty
        | NEXT_SYM FROM
        | FROM
        ;

sp_fetch_list:
          ident
          {
            LEX *lex= Lex;
            sp_head *sp= lex->sphead;
            sp_pcontext *pctx= lex->get_sp_current_parsing_ctx();
            sp_variable *spv;

            if (!pctx || !(spv= pctx->find_variable($1.str, $1.length, false)))
            {
              my_error(ER_SP_UNDECLARED_VAR, MYF(0), $1.str);
              MYSQL_YYABORT;
            }

            /* An SP local variable */
            sp_instr_cfetch *i= (sp_instr_cfetch *)sp->last_instruction();

            i->add_to_varlist(spv);
          }
        | sp_fetch_list ',' ident
          {
            LEX *lex= Lex;
            sp_head *sp= lex->sphead;
            sp_pcontext *pctx= lex->get_sp_current_parsing_ctx();
            sp_variable *spv;

            if (!pctx || !(spv= pctx->find_variable($3.str, $3.length, false)))
            {
              my_error(ER_SP_UNDECLARED_VAR, MYF(0), $3.str);
              MYSQL_YYABORT;
            }

            /* An SP local variable */
            sp_instr_cfetch *i= (sp_instr_cfetch *)sp->last_instruction();

            i->add_to_varlist(spv);
          }
        ;

sp_if:
          {                     /*$1*/
            THD *thd= YYTHD;
            LEX *lex= thd->lex;
            sp_head *sp= lex->sphead;

            sp->reset_lex(thd);
          }
          expr                  /*$2*/
          {                     /*$3*/
            ITEMIZE($2, &$2);

            THD *thd= YYTHD;
            LEX *lex= Lex;
            sp_head *sp= lex->sphead;
            sp_pcontext *pctx= lex->get_sp_current_parsing_ctx();

            /* Extract expression string. */

            LEX_CSTRING expr_query= EMPTY_CSTR;
            const char *expr_start_ptr= @0.raw.end;

            if (lex->is_metadata_used())
            {
              expr_query= make_string(thd, expr_start_ptr, @2.raw.end);
              if (!expr_query.str)
                MYSQL_YYABORT;
            }

            sp_instr_jump_if_not *i =
              NEW_PTN sp_instr_jump_if_not(sp->instructions(), lex,
                                           $2, expr_query);

            /* Add jump instruction. */

            if (i == nullptr ||
                sp->m_parser_data.add_backpatch_entry(
                  i, pctx->push_label(thd, EMPTY_CSTR, 0)) ||
                sp->m_parser_data.add_cont_backpatch_entry(i) ||
                sp->add_instr(thd, i) ||
                sp->restore_lex(thd))
            {
              MYSQL_YYABORT;
            }
          }
          THEN_SYM              /*$4*/
          sp_proc_stmts1        /*$5*/
          {                     /*$6*/
            THD *thd= YYTHD;
            LEX *lex= thd->lex;
            sp_head *sp= lex->sphead;
            sp_pcontext *pctx= lex->get_sp_current_parsing_ctx();

            sp_instr_jump *i = NEW_PTN sp_instr_jump(sp->instructions(), pctx);

            if (!i || sp->add_instr(thd, i))
              MYSQL_YYABORT;

            sp->m_parser_data.do_backpatch(pctx->pop_label(),
                                           sp->instructions());

            sp->m_parser_data.add_backpatch_entry(
              i, pctx->push_label(thd, EMPTY_CSTR, 0));
          }
          sp_elseifs            /*$7*/
          {                     /*$8*/
            LEX *lex= Lex;
            sp_head *sp= lex->sphead;
            sp_pcontext *pctx= lex->get_sp_current_parsing_ctx();

            sp->m_parser_data.do_backpatch(pctx->pop_label(),
                                           sp->instructions());
          }
        ;

sp_elseifs:
          %empty
        | ELSEIF_SYM sp_if
        | ELSE sp_proc_stmts1
        ;

case_stmt_specification:
          simple_case_stmt
        | searched_case_stmt
        ;

simple_case_stmt:
          CASE_SYM                      /*$1*/
          {                             /*$2*/
            THD *thd= YYTHD;
            LEX *lex= thd->lex;
            sp_head *sp= lex->sphead;

            case_stmt_action_case(thd);

            sp->reset_lex(thd); /* For CASE-expr $3 */
          }
          expr                          /*$3*/
          {                             /*$4*/
            ITEMIZE($3, &$3);

            THD *thd= YYTHD;
            LEX *lex= Lex;
            sp_head *sp= lex->sphead;

            /* Extract CASE-expression string. */

            LEX_CSTRING case_expr_query= EMPTY_CSTR;
            const char *expr_start_ptr= @1.raw.end;

            if (lex->is_metadata_used())
            {
              case_expr_query= make_string(thd, expr_start_ptr, @3.raw.end);
              if (!case_expr_query.str)
                MYSQL_YYABORT;
            }

            /* Register new CASE-expression and get its id. */

            sp_pcontext *pctx= lex->get_sp_current_parsing_ctx();
            int case_expr_id= pctx->push_case_expr_id();

            if (case_expr_id < 0)
              MYSQL_YYABORT;

            /* Add CASE-set instruction. */

            sp_instr_set_case_expr *i=
              NEW_PTN sp_instr_set_case_expr(sp->instructions(), lex,
                                             case_expr_id, $3, case_expr_query);

            if (i == nullptr ||
                sp->m_parser_data.add_cont_backpatch_entry(i) ||
                sp->add_instr(thd, i) ||
                sp->restore_lex(thd))
            {
              MYSQL_YYABORT;
            }
          }
          simple_when_clause_list       /*$5*/
          else_clause_opt               /*$6*/
          END                           /*$7*/
          CASE_SYM                      /*$8*/
          {                             /*$9*/
            case_stmt_action_end_case(Lex, true);
          }
        ;

searched_case_stmt:
          CASE_SYM
          {
            case_stmt_action_case(YYTHD);
          }
          searched_when_clause_list
          else_clause_opt
          END
          CASE_SYM
          {
            case_stmt_action_end_case(Lex, false);
          }
        ;

simple_when_clause_list:
          simple_when_clause
        | simple_when_clause_list simple_when_clause
        ;

searched_when_clause_list:
          searched_when_clause
        | searched_when_clause_list searched_when_clause
        ;

simple_when_clause:
          WHEN_SYM                      /*$1*/
          {                             /*$2*/
            THD *thd= YYTHD;
            LEX *lex= thd->lex;
            sp_head *sp= lex->sphead;

            sp->reset_lex(thd);
          }
          expr                          /*$3*/
          {                             /*$4*/
            /* Simple case: <caseval> = <whenval> */

            ITEMIZE($3, &$3);

            THD *thd= YYTHD;
            LEX *lex= thd->lex;
            sp_head *sp= lex->sphead;
            sp_pcontext *pctx= lex->get_sp_current_parsing_ctx();

            /* Extract expression string. */

            LEX_CSTRING when_expr_query= EMPTY_CSTR;
            const char *expr_start_ptr= @1.raw.end;

            if (lex->is_metadata_used())
            {
              when_expr_query= make_string(thd, expr_start_ptr, @3.raw.end);
              if (!when_expr_query.str)
                MYSQL_YYABORT;
            }

            /* Add CASE-when-jump instruction. */

            sp_instr_jump_case_when *i =
              NEW_PTN sp_instr_jump_case_when(sp->instructions(), lex,
                                              pctx->get_current_case_expr_id(),
                                              $3, when_expr_query);

            if (i == nullptr ||
                i->on_after_expr_parsing(thd) ||
                sp->m_parser_data.add_backpatch_entry(
                  i, pctx->push_label(thd, EMPTY_CSTR, 0)) ||
                sp->m_parser_data.add_cont_backpatch_entry(i) ||
                sp->add_instr(thd, i) ||
                sp->restore_lex(thd))
            {
              MYSQL_YYABORT;
            }
          }
          THEN_SYM                      /*$5*/
          sp_proc_stmts1                /*$6*/
          {                             /*$7*/
            if (case_stmt_action_then(YYTHD, Lex))
              MYSQL_YYABORT;
          }
        ;

searched_when_clause:
          WHEN_SYM                      /*$1*/
          {                             /*$2*/
            THD *thd= YYTHD;
            LEX *lex= thd->lex;
            sp_head *sp= lex->sphead;

            sp->reset_lex(thd);
          }
          expr                          /*$3*/
          {                             /*$4*/
            ITEMIZE($3, &$3);

            THD *thd= YYTHD;
            LEX *lex= thd->lex;
            sp_head *sp= lex->sphead;
            sp_pcontext *pctx= lex->get_sp_current_parsing_ctx();

            /* Extract expression string. */

            LEX_CSTRING when_query= EMPTY_CSTR;
            const char *expr_start_ptr= @1.raw.end;

            if (lex->is_metadata_used())
            {
              when_query= make_string(thd, expr_start_ptr, @3.raw.end);
              if (!when_query.str)
                MYSQL_YYABORT;
            }

            /* Add jump instruction. */

            sp_instr_jump_if_not *i=
              NEW_PTN sp_instr_jump_if_not(sp->instructions(), lex, $3,
                                           when_query);

            if (i == nullptr ||
                sp->m_parser_data.add_backpatch_entry(
                  i, pctx->push_label(thd, EMPTY_CSTR, 0)) ||
                sp->m_parser_data.add_cont_backpatch_entry(i) ||
                sp->add_instr(thd, i) ||
                sp->restore_lex(thd))
            {
              MYSQL_YYABORT;
            }
          }
          THEN_SYM                      /*$6*/
          sp_proc_stmts1                /*$7*/
          {                             /*$8*/
            if (case_stmt_action_then(YYTHD, Lex))
              MYSQL_YYABORT;
          }
        ;

else_clause_opt:
          %empty
          {
            THD *thd= YYTHD;
            LEX *lex= Lex;
            sp_head *sp= lex->sphead;
            sp_pcontext *pctx= lex->get_sp_current_parsing_ctx();

            sp_instr_error *i=
              NEW_PTN
                sp_instr_error(sp->instructions(), pctx, ER_SP_CASE_NOT_FOUND);

            if (!i || sp->add_instr(thd, i))
              MYSQL_YYABORT;
          }
        | ELSE sp_proc_stmts1
        ;

sp_labeled_control:
          label_ident ':'
          {
            LEX *lex= Lex;
            sp_head *sp= lex->sphead;
            sp_pcontext *pctx= lex->get_sp_current_parsing_ctx();
            sp_label *lab= pctx->find_label($1);

            if (lab)
            {
              my_error(ER_SP_LABEL_REDEFINE, MYF(0), $1.str);
              MYSQL_YYABORT;
            }
            else
            {
              lab= pctx->push_label(YYTHD, $1, sp->instructions());
              lab->type= sp_label::ITERATION;
            }
          }
          sp_unlabeled_control sp_opt_label
          {
            LEX *lex= Lex;
            sp_head *sp= lex->sphead;
            sp_pcontext *pctx= lex->get_sp_current_parsing_ctx();
            sp_label *lab= pctx->pop_label();

            if ($5.str)
            {
              if (my_strcasecmp(system_charset_info, $5.str, lab->name.str) != 0)
              {
                my_error(ER_SP_LABEL_MISMATCH, MYF(0), $5.str);
                MYSQL_YYABORT;
              }
            }
            sp->m_parser_data.do_backpatch(lab, sp->instructions());
          }
        ;

sp_opt_label:
          %empty { $$= NULL_CSTR; }
        | label_ident   { $$= $1; }
        ;

sp_labeled_block:
          label_ident ':'
          {
            LEX *lex= Lex;
            sp_head *sp= lex->sphead;
            sp_pcontext *pctx= lex->get_sp_current_parsing_ctx();
            sp_label *lab= pctx->find_label($1);

            if (lab)
            {
              my_error(ER_SP_LABEL_REDEFINE, MYF(0), $1.str);
              MYSQL_YYABORT;
            }

            lab= pctx->push_label(YYTHD, $1, sp->instructions());
            lab->type= sp_label::BEGIN;
          }
          sp_block_content sp_opt_label
          {
            LEX *lex= Lex;
            sp_pcontext *pctx= lex->get_sp_current_parsing_ctx();
            sp_label *lab= pctx->pop_label();

            if ($5.str)
            {
              if (my_strcasecmp(system_charset_info, $5.str, lab->name.str) != 0)
              {
                my_error(ER_SP_LABEL_MISMATCH, MYF(0), $5.str);
                MYSQL_YYABORT;
              }
            }
          }
        ;

sp_unlabeled_block:
          { /* Unlabeled blocks get a secret label. */
            LEX *lex= Lex;
            sp_head *sp= lex->sphead;
            sp_pcontext *pctx= lex->get_sp_current_parsing_ctx();

            sp_label *lab=
              pctx->push_label(YYTHD, EMPTY_CSTR, sp->instructions());

            lab->type= sp_label::BEGIN;
          }
          sp_block_content
          {
            LEX *lex= Lex;
            lex->get_sp_current_parsing_ctx()->pop_label();
          }
        ;

sp_block_content:
          BEGIN_SYM
          { /* QQ This is just a dummy for grouping declarations and statements
              together. No [[NOT] ATOMIC] yet, and we need to figure out how
              make it coexist with the existing BEGIN COMMIT/ROLLBACK. */
            THD *thd= YYTHD;
            LEX *lex= thd->lex;
            sp_pcontext *parent_pctx= lex->get_sp_current_parsing_ctx();

            sp_pcontext *child_pctx=
              parent_pctx->push_context(thd, sp_pcontext::REGULAR_SCOPE);

            lex->set_sp_current_parsing_ctx(child_pctx);
          }
          sp_decls
          sp_proc_stmts
          END
          {
            THD *thd= YYTHD;
            LEX *lex= Lex;
            sp_head *sp= lex->sphead;
            sp_pcontext *pctx= lex->get_sp_current_parsing_ctx();

            // We always have a label.
            sp->m_parser_data.do_backpatch(pctx->last_label(),
                                           sp->instructions());

            if ($3.hndlrs)
            {
              sp_instr *i= NEW_PTN sp_instr_hpop(sp->instructions(), pctx);

              if (!i || sp->add_instr(thd, i))
                MYSQL_YYABORT;
            }

            if ($3.curs)
            {
              sp_instr *i= NEW_PTN sp_instr_cpop(sp->instructions(), pctx,
                                                 $3.curs);

              if (!i || sp->add_instr(thd, i))
                MYSQL_YYABORT;
            }

            lex->set_sp_current_parsing_ctx(pctx->pop_context());
          }
        ;

sp_unlabeled_control:
          LOOP_SYM
          sp_proc_stmts1 END LOOP_SYM
          {
            THD *thd= YYTHD;
            LEX *lex= Lex;
            sp_head *sp= lex->sphead;
            sp_pcontext *pctx= lex->get_sp_current_parsing_ctx();

            sp_instr_jump *i= NEW_PTN sp_instr_jump(sp->instructions(), pctx,
                                                    pctx->last_label()->ip);

            if (!i || sp->add_instr(thd, i))
              MYSQL_YYABORT;
          }
        | WHILE_SYM                     /*$1*/
          {                             /*$2*/
            THD *thd= YYTHD;
            LEX *lex= thd->lex;
            sp_head *sp= lex->sphead;

            sp->reset_lex(thd);
          }
          expr                          /*$3*/
          {                             /*$4*/
            ITEMIZE($3, &$3);

            THD *thd= YYTHD;
            LEX *lex= Lex;
            sp_head *sp= lex->sphead;
            sp_pcontext *pctx= lex->get_sp_current_parsing_ctx();

            /* Extract expression string. */

            LEX_CSTRING expr_query= EMPTY_CSTR;
            const char *expr_start_ptr= @1.raw.end;

            if (lex->is_metadata_used())
            {
              expr_query= make_string(thd, expr_start_ptr, @3.raw.end);
              if (!expr_query.str)
                MYSQL_YYABORT;
            }

            /* Add jump instruction. */

            sp_instr_jump_if_not *i=
              NEW_PTN
                sp_instr_jump_if_not(sp->instructions(), lex, $3, expr_query);

            if (i == nullptr ||
                /* Jumping forward */
                sp->m_parser_data.add_backpatch_entry(i, pctx->last_label()) ||
                sp->m_parser_data.new_cont_backpatch() ||
                sp->m_parser_data.add_cont_backpatch_entry(i) ||
                sp->add_instr(thd, i) ||
                sp->restore_lex(thd))
            {
              MYSQL_YYABORT;
            }
          }
          DO_SYM                        /*$10*/
          sp_proc_stmts1                /*$11*/
          END                           /*$12*/
          WHILE_SYM                     /*$13*/
          {                             /*$14*/
            THD *thd= YYTHD;
            LEX *lex= Lex;
            sp_head *sp= lex->sphead;
            sp_pcontext *pctx= lex->get_sp_current_parsing_ctx();

            sp_instr_jump *i= NEW_PTN sp_instr_jump(sp->instructions(), pctx,
                                                    pctx->last_label()->ip);

            if (!i || sp->add_instr(thd, i))
              MYSQL_YYABORT;

            sp->m_parser_data.do_cont_backpatch(sp->instructions());
          }
        | REPEAT_SYM                    /*$1*/
          sp_proc_stmts1                /*$2*/
          UNTIL_SYM                     /*$3*/
          {                             /*$4*/
            THD *thd= YYTHD;
            LEX *lex= thd->lex;
            sp_head *sp= lex->sphead;

            sp->reset_lex(thd);
          }
          expr                          /*$5*/
          {                             /*$6*/
            ITEMIZE($5, &$5);

            THD *thd= YYTHD;
            LEX *lex= thd->lex;
            sp_head *sp= lex->sphead;
            sp_pcontext *pctx= lex->get_sp_current_parsing_ctx();
            uint ip= sp->instructions();

            /* Extract expression string. */

            LEX_CSTRING expr_query= EMPTY_CSTR;
            const char *expr_start_ptr= @3.raw.end;

            if (lex->is_metadata_used())
            {
              expr_query= make_string(thd, expr_start_ptr, @5.raw.end);
              if (!expr_query.str)
                MYSQL_YYABORT;
            }

            /* Add jump instruction. */

            sp_instr_jump_if_not *i=
              NEW_PTN sp_instr_jump_if_not(ip, lex, $5, expr_query,
                                           pctx->last_label()->ip);

            if (i == nullptr ||
                sp->add_instr(thd, i) ||
                sp->restore_lex(thd))
            {
              MYSQL_YYABORT;
            }

            /* We can shortcut the cont_backpatch here */
            i->set_cont_dest(ip + 1);
          }
          END                           /*$7*/
          REPEAT_SYM                    /*$8*/
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

opt_undo_tablespace_options:
          %empty { $$= nullptr; }
        | undo_tablespace_option_list
        ;

undo_tablespace_option_list:
          undo_tablespace_option
          {
            $$= NEW_PTN Mem_root_array<PT_alter_tablespace_option_base*>(YYMEM_ROOT);
            if ($$ == nullptr || $$->push_back($1))
              MYSQL_YYABORT; // OOM
          }
        | undo_tablespace_option_list opt_comma undo_tablespace_option
          {
            $$= $1;
            if ($$->push_back($3))
              MYSQL_YYABORT; // OOM
          }
        ;

undo_tablespace_option:
          ts_option_engine
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

ts_option_autoextend_size:
          option_autoextend_size
          {
            $$ = NEW_PTN PT_alter_tablespace_option_autoextend_size(@$, $1);
          }
        ;

option_autoextend_size:
          AUTOEXTEND_SIZE_SYM opt_equal size_number { $$ = $3; }
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

ts_option_engine:
          opt_storage ENGINE_SYM opt_equal ident_or_text
          {
            $$= NEW_PTN PT_alter_tablespace_option_engine(@$, to_lex_cstring($4));
          }
        ;

ts_option_file_block_size:
          FILE_BLOCK_SIZE_SYM opt_equal size_number
          {
            $$= NEW_PTN PT_alter_tablespace_option_file_block_size(@$, $3);
          }
        ;

ts_option_wait:
          WAIT_SYM
          {
            $$= NEW_PTN PT_alter_tablespace_option_wait_until_completed(@$, true);
          }
        | NO_WAIT_SYM
          {
            $$= NEW_PTN PT_alter_tablespace_option_wait_until_completed(@$, false);
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

size_number:
          real_ulonglong_num { $$= $1;}
        | IDENT_sys
          {
            ulonglong number;
            uint text_shift_number= 0;
            longlong prefix_number;
            const char *start_ptr= $1.str;
            size_t str_len= $1.length;
            const char *end_ptr= start_ptr + str_len;
            int error;
            prefix_number= my_strtoll10(start_ptr, &end_ptr, &error);
            if ((start_ptr + str_len - 1) == end_ptr)
            {
              switch (end_ptr[0])
              {
                case 'g':
                case 'G':
                  text_shift_number+=10;
                  [[fallthrough]];
                case 'm':
                case 'M':
                  text_shift_number+=10;
                  [[fallthrough]];
                case 'k':
                case 'K':
                  text_shift_number+=10;
                  break;
                default:
                {
                  my_error(ER_WRONG_SIZE_NUMBER, MYF(0));
                  MYSQL_YYABORT;
                }
              }
              if (prefix_number >> 31)
              {
                my_error(ER_SIZE_OVERFLOW_ERROR, MYF(0));
                MYSQL_YYABORT;
              }
              number= prefix_number << text_shift_number;
            }
            else
            {
              my_error(ER_WRONG_SIZE_NUMBER, MYF(0));
              MYSQL_YYABORT;
            }
            $$= number;
          }
        ;

/*
  End tablespace part
*/

/*
  To avoid grammar conflicts, we introduce the next few rules in very details:
  we workaround empty rules for optional AS and DUPLICATE clauses by expanding
  them in place of the caller rule:

  opt_create_table_options_etc ::=
    create_table_options opt_create_partitioning_etc
  | opt_create_partitioning_etc

  opt_create_partitioning_etc ::=
    partitioin [opt_duplicate_as_qe] | [opt_duplicate_as_qe]

  opt_duplicate_as_qe ::=
    duplicate as_create_query_expression
  | as_create_query_expression

  as_create_query_expression ::=
    AS query_expression_with_opt_locking_clauses
  | query_expression_with_opt_locking_clauses

*/

opt_create_table_options_etc:
          create_table_options
          opt_create_partitioning_etc
          {
            $$= $2;
            $$.opt_create_table_options= $1;
          }
        | opt_create_partitioning_etc
        ;

opt_create_partitioning_etc:
          partition_clause opt_duplicate_as_qe
          {
            $$= $2;
            $$.opt_partitioning= $1;
          }
        | opt_duplicate_as_qe
        ;

opt_duplicate_as_qe:
          %empty
          {
            $$.opt_create_table_options= nullptr;
            $$.opt_partitioning= nullptr;
            $$.on_duplicate= On_duplicate::ERROR;
            $$.opt_query_expression= nullptr;
          }
        | duplicate
          as_create_query_expression
          {
            $$.opt_create_table_options= nullptr;
            $$.opt_partitioning= nullptr;
            $$.on_duplicate= $1;
            $$.opt_query_expression= $2;
          }
        | as_create_query_expression
          {
            $$.opt_create_table_options= nullptr;
            $$.opt_partitioning= nullptr;
            $$.on_duplicate= On_duplicate::ERROR;
            $$.opt_query_expression= $1;
          }
        ;

as_create_query_expression:
          AS query_expression_with_opt_locking_clauses { $$ = $2; }
        | query_expression_with_opt_locking_clauses    { $$ = $1; }
        ;

/*
 This part of the parser is about handling of the partition information.

 It's first version was written by Mikael Ronström with lots of answers to
 questions provided by Antony Curtis.

 The partition grammar can be called from two places.
 1) CREATE TABLE ... PARTITION ..
 2) ALTER TABLE table_name PARTITION ...
*/
partition_clause:
          PARTITION_SYM BY part_type_def opt_num_parts opt_sub_part
          opt_part_defs
          {
            $$= NEW_PTN PT_partition(@$, $3, $4, $5, @6, $6);
          }
        ;

part_type_def:
          opt_linear KEY_SYM opt_key_algo '(' opt_name_list ')'
          {
            $$= NEW_PTN PT_part_type_def_key(@$, $1, $3, $5);
          }
        | opt_linear HASH_SYM '(' bit_expr ')'
          {
            $$= NEW_PTN PT_part_type_def_hash(@$, $1, @4, $4);
          }
        | RANGE_SYM '(' bit_expr ')'
          {
            $$= NEW_PTN PT_part_type_def_range_expr(@$, @3, $3);
          }
        | RANGE_SYM COLUMNS '(' name_list ')'
          {
            $$= NEW_PTN PT_part_type_def_range_columns(@$, $4);
          }
        | LIST_SYM '(' bit_expr ')'
          {
            $$= NEW_PTN PT_part_type_def_list_expr(@$, @3, $3);
          }
        | LIST_SYM COLUMNS '(' name_list ')'
          {
            $$= NEW_PTN PT_part_type_def_list_columns(@$, $4);
          }
        ;

opt_linear:
          %empty { $$= false; }
        | LINEAR_SYM  { $$= true; }
        ;

opt_key_algo:
          %empty { $$= enum_key_algorithm::KEY_ALGORITHM_NONE; }
        | ALGORITHM_SYM EQ real_ulong_num
          {
            switch ($3) {
            case 1:
              $$= enum_key_algorithm::KEY_ALGORITHM_51;
              break;
            case 2:
              $$= enum_key_algorithm::KEY_ALGORITHM_55;
              break;
            default:
              YYTHD->syntax_error();
              MYSQL_YYABORT;
            }
          }
        ;

opt_num_parts:
          %empty { $$= 0; }
        | PARTITIONS_SYM real_ulong_num
          {
            if ($2 == 0)
            {
              my_error(ER_NO_PARTS_ERROR, MYF(0), "partitions");
              MYSQL_YYABORT;
            }
            $$= $2;
          }
        ;

opt_sub_part:
          %empty { $$= nullptr; }
        | SUBPARTITION_SYM BY opt_linear HASH_SYM '(' bit_expr ')'
          opt_num_subparts
          {
            $$= NEW_PTN PT_sub_partition_by_hash(@$, $3, @6, $6, $8);
          }
        | SUBPARTITION_SYM BY opt_linear KEY_SYM opt_key_algo
          '(' name_list ')' opt_num_subparts
          {
            $$= NEW_PTN PT_sub_partition_by_key(@$, $3, $5, $7, $9);
          }
        ;


opt_name_list:
          %empty { $$= nullptr; }
        | name_list
        ;


name_list:
          ident
          {
            $$= NEW_PTN List<char>;
            if ($$ == nullptr || $$->push_back($1.str))
              MYSQL_YYABORT;
          }
        | name_list ',' ident
          {
            $$= $1;
            if ($$->push_back($3.str))
              MYSQL_YYABORT;
          }
        ;

opt_num_subparts:
          %empty { $$= 0; }
        | SUBPARTITIONS_SYM real_ulong_num
          {
            if ($2 == 0)
            {
              my_error(ER_NO_PARTS_ERROR, MYF(0), "subpartitions");
              MYSQL_YYABORT;
            }
            $$= $2;
          }
        ;

opt_part_defs:
          %empty { $$= nullptr; }
        | '(' part_def_list ')' { $$= $2; }
        ;

part_def_list:
          part_definition
          {
            $$= NEW_PTN Mem_root_array<PT_part_definition*>(YYMEM_ROOT);
            if ($$ == nullptr || $$->push_back($1))
              MYSQL_YYABORT; // OOM
          }
        | part_def_list ',' part_definition
          {
            $$= $1;
            if ($$->push_back($3))
              MYSQL_YYABORT; // OOM
          }
        ;

part_definition:
          PARTITION_SYM ident opt_part_values opt_part_options opt_sub_partition
          {
            $$= NEW_PTN PT_part_definition(@$, @0, $2, $3.type, $3.values, @3,
                                           $4, $5, @5);
          }
        ;

opt_part_values:
          %empty
          {
            $$.type= partition_type::HASH;
          }
        | VALUES LESS_SYM THAN_SYM part_func_max
          {
            $$.type= partition_type::RANGE;
            $$.values= $4;
          }
        | VALUES IN_SYM part_values_in
          {
            $$.type= partition_type::LIST;
            $$.values= $3;
          }
        ;

part_func_max:
          MAX_VALUE_SYM   { $$= nullptr; }
        | part_value_item_list_paren
        ;

part_values_in:
          part_value_item_list_paren
          {
            $$= NEW_PTN PT_part_values_in_item(@$, @1, $1);
          }
        | '(' part_value_list ')'
          {
            $$= NEW_PTN PT_part_values_in_list(@$, @3, $2);
          }
        ;

part_value_list:
          part_value_item_list_paren
          {
            $$= NEW_PTN
              Mem_root_array<PT_part_value_item_list_paren *>(YYMEM_ROOT);
            if ($$ == nullptr || $$->push_back($1))
              MYSQL_YYABORT; // OOM
          }
        | part_value_list ',' part_value_item_list_paren
          {
            $$= $1;
            if ($$->push_back($3))
              MYSQL_YYABORT; // OOM
          }
        ;

part_value_item_list_paren:
          '('
          {
            /*
              This empty action is required because it resolves 2 reduce/reduce
              conflicts with an anonymous row expression:

              simple_expr:
                        ...
                      | '(' expr ',' expr_list ')'
            */
          }
          part_value_item_list ')'
          {
            $$= NEW_PTN PT_part_value_item_list_paren(@$, $3, @4);
          }
        ;

part_value_item_list:
          part_value_item
          {
            $$= NEW_PTN Mem_root_array<PT_part_value_item *>(YYMEM_ROOT);
            if ($$ == nullptr || $$->push_back($1))
              MYSQL_YYABORT; // OOM
          }
        | part_value_item_list ',' part_value_item
          {
            $$= $1;
            if ($$->push_back($3))
              MYSQL_YYABORT; // OOM
          }
        ;

part_value_item:
          MAX_VALUE_SYM { $$= NEW_PTN PT_part_value_item_max(@$); }
        | bit_expr      { $$= NEW_PTN PT_part_value_item_expr(@$, $1); }
        ;


opt_sub_partition:
          %empty { $$= nullptr; }
        | '(' sub_part_list ')' { $$= $2; }
        ;

sub_part_list:
          sub_part_definition
          {
            $$= NEW_PTN Mem_root_array<PT_subpartition *>(YYMEM_ROOT);
            if ($$ == nullptr || $$->push_back($1))
              MYSQL_YYABORT; // OOM
          }
        | sub_part_list ',' sub_part_definition
          {
            $$= $1;
            if ($$->push_back($3))
              MYSQL_YYABORT; // OOM
          }
        ;

sub_part_definition:
          SUBPARTITION_SYM ident_or_text opt_part_options
          {
            $$= NEW_PTN PT_subpartition(@$, @1, $2.str, $3);
          }
        ;

opt_part_options:
         %empty { $$= nullptr; }
       | part_option_list
       ;

part_option_list:
          part_option_list part_option
          {
            $$= $1;
            if ($$->push_back($2))
              MYSQL_YYABORT; // OOM
          }
        | part_option
          {
            $$= NEW_PTN Mem_root_array<PT_partition_option *>(YYMEM_ROOT);
            if ($$ == nullptr || $$->push_back($1))
              MYSQL_YYABORT; // OOM
          }
        ;

part_option:
          TABLESPACE_SYM opt_equal ident
          { $$= NEW_PTN PT_partition_tablespace(@$, $3.str); }
        | opt_storage ENGINE_SYM opt_equal ident_or_text
          { $$= NEW_PTN PT_partition_engine(@$, to_lex_cstring($4)); }
        | NODEGROUP_SYM opt_equal real_ulong_num
          { $$= NEW_PTN PT_partition_nodegroup(@$, $3); }
        | MAX_ROWS opt_equal real_ulonglong_num
          { $$= NEW_PTN PT_partition_max_rows(@$, $3); }
        | MIN_ROWS opt_equal real_ulonglong_num
          { $$= NEW_PTN PT_partition_min_rows(@$, $3); }
        | DATA_SYM DIRECTORY_SYM opt_equal TEXT_STRING_sys
          { $$= NEW_PTN PT_partition_data_directory(@$, $4.str); }
        | INDEX_SYM DIRECTORY_SYM opt_equal TEXT_STRING_sys
          { $$= NEW_PTN PT_partition_index_directory(@$, $4.str); }
        | COMMENT_SYM opt_equal TEXT_STRING_sys
          { $$= NEW_PTN PT_partition_comment(@$, $3.str); }
        ;

/*
 End of partition parser part
*/

alter_database_options:
          alter_database_option
        | alter_database_options alter_database_option
        ;

alter_database_option:
          create_database_option
        | READ_SYM ONLY_SYM opt_equal ternary_option
          {
            /*
              If the statement has set READ ONLY already, and we repeat the
              READ ONLY option in the statement, the option must be set to
              the same value as before, otherwise, report an error.
            */
            if ((Lex->create_info->used_fields &
                 HA_CREATE_USED_READ_ONLY) &&
                (Lex->create_info->schema_read_only !=
                    ($4 == Ternary_option::ON))) {
              my_error(ER_CONFLICTING_DECLARATIONS, MYF(0), "READ ONLY", "=0",
                  "READ ONLY", "=1");
              MYSQL_YYABORT;
            }
            Lex->create_info->schema_read_only = ($4 == Ternary_option::ON);
            Lex->create_info->used_fields |= HA_CREATE_USED_READ_ONLY;
          }
        ;

opt_create_database_options:
          %empty {}
        | create_database_options {}
        ;

create_database_options:
          create_database_option {}
        | create_database_options create_database_option {}
        ;

create_database_option:
          default_collation
          {
            if (set_default_collation(Lex->create_info, $1))
              MYSQL_YYABORT;
          }
        | default_charset
          {
            if (set_default_charset(Lex->create_info, $1))
              MYSQL_YYABORT;
          }
        | default_encryption
          {
            // Validate if we have either 'y|Y' or 'n|N'
            if (my_strcasecmp(system_charset_info, $1.str, "Y") != 0 &&
                my_strcasecmp(system_charset_info, $1.str, "N") != 0) {
              my_error(ER_WRONG_VALUE, MYF(0), "argument (should be Y or N)", $1.str);
              MYSQL_YYABORT;
            }

            Lex->create_info->encrypt_type= $1;
            Lex->create_info->used_fields |= HA_CREATE_USED_DEFAULT_ENCRYPTION;
          }
        ;

opt_if_not_exists:
          %empty { $$= false; }
        | IF not EXISTS { $$= true; }
        ;

create_table_options_space_separated:
          create_table_option
          {
            $$= NEW_PTN Mem_root_array<PT_ddl_table_option *>(YYMEM_ROOT);
            if ($$ == nullptr || $$->push_back($1))
              MYSQL_YYABORT; // OOM
          }
        | create_table_options_space_separated create_table_option
          {
            $$= $1;
            if ($$->push_back($2))
              MYSQL_YYABORT; // OOM
          }
        ;

create_table_options:
          create_table_option
          {
            $$= NEW_PTN Mem_root_array<PT_create_table_option *>(YYMEM_ROOT);
            if ($$ == nullptr || $$->push_back($1))
              MYSQL_YYABORT; // OOM
          }
        | create_table_options opt_comma create_table_option
          {
            $$= $1;
            if ($$->push_back($3))
              MYSQL_YYABORT; // OOM
          }
        ;

opt_comma:
          %empty
        | ','
        ;

create_table_option:
          ENGINE_SYM opt_equal ident_or_text
          {
            $$= NEW_PTN PT_create_table_engine_option(@$, to_lex_cstring($3));
          }
        | SECONDARY_ENGINE_SYM opt_equal NULL_SYM
          {
            $$= NEW_PTN PT_create_table_secondary_engine_option(@$);
          }
        | SECONDARY_ENGINE_SYM opt_equal ident_or_text
          {
            $$= NEW_PTN PT_create_table_secondary_engine_option(@$, to_lex_cstring($3));
          }
        | MAX_ROWS opt_equal ulonglong_num
          {
            $$= NEW_PTN PT_create_max_rows_option(@$, $3);
          }
        | MIN_ROWS opt_equal ulonglong_num
          {
            $$= NEW_PTN PT_create_min_rows_option(@$, $3);
          }
        | AVG_ROW_LENGTH opt_equal ulonglong_num
          {
            // The frm-format only allocated 4 bytes for avg_row_length, and
            // there is code which assumes it can be represented as an uint,
            // so we constrain it here.
            if ($3 > std::numeric_limits<std::uint32_t>::max()) {
              YYTHD->syntax_error_at(@3,
              "The valid range for avg_row_length is [0,4294967295]. Error"
              );
              MYSQL_YYABORT;
            }
            $$= NEW_PTN PT_create_avg_row_length_option(@$, $3);
          }
        | PASSWORD opt_equal TEXT_STRING_sys
          {
            $$= NEW_PTN PT_create_password_option(@$, $3.str);
          }
        | COMMENT_SYM opt_equal TEXT_STRING_sys
          {
            $$= NEW_PTN PT_create_commen_option(@$, $3);
          }
        | COMPRESSION_SYM opt_equal TEXT_STRING_sys
          {
            $$= NEW_PTN PT_create_compress_option(@$, $3);
          }
        | ENCRYPTION_SYM opt_equal TEXT_STRING_sys
          {
            $$= NEW_PTN PT_create_encryption_option(@$, $3);
          }
        | AUTO_INC opt_equal ulonglong_num
          {
            $$= NEW_PTN PT_create_auto_increment_option(@$, $3);
          }
        | PACK_KEYS_SYM opt_equal ternary_option
          {
            $$= NEW_PTN PT_create_pack_keys_option(@$, $3);
          }
        | STATS_AUTO_RECALC_SYM opt_equal ternary_option
          {
            $$= NEW_PTN PT_create_stats_auto_recalc_option(@$, $3);
          }
        | STATS_PERSISTENT_SYM opt_equal ternary_option
          {
            $$= NEW_PTN PT_create_stats_persistent_option(@$, $3);
          }
        | STATS_SAMPLE_PAGES_SYM opt_equal ulong_num
          {
            /* From user point of view STATS_SAMPLE_PAGES can be specified as
            STATS_SAMPLE_PAGES=N (where 0<N<=65535, it does not make sense to
            scan 0 pages) or STATS_SAMPLE_PAGES=default. Internally we record
            =default as 0. See create_frm() in sql/table.cc, we use only two
            bytes for stats_sample_pages and this is why we do not allow
            larger values. 65535 pages, 16kb each means to sample 1GB, which
            is impractical. If at some point this needs to be extended, then
            we can store the higher bits from stats_sample_pages in .frm too. */
            if ($3 == 0 || $3 > 0xffff)
            {
              YYTHD->syntax_error_at(@3,
              "The valid range for stats_sample_pages is [1, 65535]. Error");
              MYSQL_YYABORT;
            }
            $$= NEW_PTN PT_create_stats_stable_pages(@$, $3);
          }
        | STATS_SAMPLE_PAGES_SYM opt_equal DEFAULT_SYM
          {
            $$= NEW_PTN PT_create_stats_stable_pages(@$);
          }
        | CHECKSUM_SYM opt_equal ulong_num
          {
            $$= NEW_PTN PT_create_checksum_option(@$, $3);
          }
        | TABLE_CHECKSUM_SYM opt_equal ulong_num
          {
            $$= NEW_PTN PT_create_checksum_option(@$, $3);
          }
        | DELAY_KEY_WRITE_SYM opt_equal ulong_num
          {
            $$= NEW_PTN PT_create_delay_key_write_option(@$, $3);
          }
        | ROW_FORMAT_SYM opt_equal row_types
          {
            $$= NEW_PTN PT_create_row_format_option(@$, $3);
          }
        | UNION_SYM opt_equal '(' opt_table_list ')'
          {
            $$= NEW_PTN PT_create_union_option(@$, $4);
          }
        | default_charset
          {
            $$= NEW_PTN PT_create_table_default_charset(@$, $1);
          }
        | default_collation
          {
            $$= NEW_PTN PT_create_table_default_collation(@$, $1);
          }
        | INSERT_METHOD opt_equal merge_insert_types
          {
            $$= NEW_PTN PT_create_insert_method_option(@$, $3);
          }
        | DATA_SYM DIRECTORY_SYM opt_equal TEXT_STRING_sys
          {
            $$= NEW_PTN PT_create_data_directory_option(@$, $4.str);
          }
        | INDEX_SYM DIRECTORY_SYM opt_equal TEXT_STRING_sys
          {
            $$= NEW_PTN PT_create_index_directory_option(@$, $4.str);
          }
        | TABLESPACE_SYM opt_equal ident
          {
            $$= NEW_PTN PT_create_tablespace_option(@$, $3.str);
          }
        | STORAGE_SYM DISK_SYM
          {
            $$= NEW_PTN PT_create_storage_option(@$, HA_SM_DISK);
          }
        | STORAGE_SYM MEMORY_SYM
          {
            $$= NEW_PTN PT_create_storage_option(@$, HA_SM_MEMORY);
          }
        | CONNECTION_SYM opt_equal TEXT_STRING_sys
          {
            $$= NEW_PTN PT_create_connection_option(@$, $3);
          }
        | KEY_BLOCK_SIZE opt_equal ulonglong_num
          {
            // The frm-format only allocated 2 bytes for key_block_size,
            // even if it is represented as std::uint32_t in HA_CREATE_INFO and
            // elsewhere.
            if ($3 > std::numeric_limits<std::uint16_t>::max()) {
              YYTHD->syntax_error_at(@3,
              "The valid range for key_block_size is [0,65535]. Error");
              MYSQL_YYABORT;
            }

            $$= NEW_PTN
            PT_create_key_block_size_option(@$, static_cast<std::uint32_t>($3));
          }
        | START_SYM TRANSACTION_SYM
          {
            $$= NEW_PTN PT_create_start_transaction_option(@$, true);
	  }
        | ENGINE_ATTRIBUTE_SYM opt_equal json_attribute
          {
            $$ = make_table_engine_attribute(YYMEM_ROOT, $3);
          }
        | SECONDARY_ENGINE_ATTRIBUTE_SYM opt_equal json_attribute
          {
            $$ = make_table_secondary_engine_attribute(YYMEM_ROOT, $3);
          }
        | option_autoextend_size
          {
            $$ = NEW_PTN PT_create_ts_autoextend_size_option(@$, $1);
          }
        ;

ternary_option:
          ulong_num
          {
            switch($1) {
            case 0:
                $$= Ternary_option::OFF;
                break;
            case 1:
                $$= Ternary_option::ON;
                break;
            default:
                YYTHD->syntax_error();
                MYSQL_YYABORT;
            }
          }
        | DEFAULT_SYM { $$= Ternary_option::DEFAULT; }
        ;

default_charset:
          opt_default character_set opt_equal charset_name { $$ = $4; }
        ;

default_collation:
          opt_default COLLATE_SYM opt_equal collation_name { $$ = $4;}
        ;

default_encryption:
          opt_default ENCRYPTION_SYM opt_equal TEXT_STRING_sys { $$ = $4;}
        ;

row_types:
          DEFAULT_SYM    { $$= ROW_TYPE_DEFAULT; }
        | FIXED_SYM      { $$= ROW_TYPE_FIXED; }
        | DYNAMIC_SYM    { $$= ROW_TYPE_DYNAMIC; }
        | COMPRESSED_SYM { $$= ROW_TYPE_COMPRESSED; }
        | REDUNDANT_SYM  { $$= ROW_TYPE_REDUNDANT; }
        | COMPACT_SYM    { $$= ROW_TYPE_COMPACT; }
        ;

merge_insert_types:
         NO_SYM          { $$= MERGE_INSERT_DISABLED; }
       | FIRST_SYM       { $$= MERGE_INSERT_TO_FIRST; }
       | LAST_SYM        { $$= MERGE_INSERT_TO_LAST; }
       ;

udf_type:
          STRING_SYM {$$ = (int) STRING_RESULT; }
        | REAL_SYM {$$ = (int) REAL_RESULT; }
        | DECIMAL_SYM {$$ = (int) DECIMAL_RESULT; }
        | INT_SYM {$$ = (int) INT_RESULT; }
        ;

table_element_list:
          table_element
          {
            $$= NEW_PTN Mem_root_array<PT_table_element *>(YYMEM_ROOT);
            if ($$ == nullptr || $$->push_back($1))
              MYSQL_YYABORT; // OOM
          }
        | table_element_list ',' table_element
          {
            $$= $1;
            if ($$->push_back($3))
              MYSQL_YYABORT; // OOM
          }
        ;

table_element:
          column_def            { $$= $1; }
        | table_constraint_def  { $$= $1; }
        ;

table_constraint_def:
          key_or_index opt_index_name_and_type '(' key_list_with_expression ')'
          opt_index_options
          {
            $$= NEW_PTN PT_inline_index_definition(@$, KEYTYPE_MULTIPLE,
                                                   $2.name, $2.type, $4, $6);
          }
        | FULLTEXT_SYM opt_key_or_index opt_ident '(' key_list_with_expression ')'
          opt_fulltext_index_options
          {
            $$= NEW_PTN PT_inline_index_definition(@$, KEYTYPE_FULLTEXT, $3, nullptr,
                                                   $5, $7);
          }
        | SPATIAL_SYM opt_key_or_index opt_ident '(' key_list_with_expression ')'
          opt_spatial_index_options
          {
            $$= NEW_PTN PT_inline_index_definition(@$, KEYTYPE_SPATIAL, $3, nullptr, $5, $7);
          }
        | opt_constraint_name constraint_key_type opt_index_name_and_type
          '(' key_list_with_expression ')' opt_index_options
          {
            /*
              Constraint-implementing indexes are named by the constraint type
              by default.
            */
            LEX_STRING name= $3.name.str != nullptr ? $3.name : $1;
            $$= NEW_PTN PT_inline_index_definition(@$, $2, name, $3.type, $5, $7);
          }
        | opt_constraint_name FOREIGN KEY_SYM opt_ident '(' key_list ')' references
          {
            $$= NEW_PTN PT_foreign_key_definition(@$, $1, $4, $6, $8.table_name,
                                                  $8.reference_list,
                                                  $8.fk_match_option,
                                                  $8.fk_update_opt,
                                                  $8.fk_delete_opt);
          }
        | opt_constraint_name check_constraint opt_constraint_enforcement
          {
            $$= NEW_PTN PT_check_constraint(@$, $1, $2, $3);
            if ($$ == nullptr) MYSQL_YYABORT; // OOM
          }
        ;

opt_not:
          %empty       { $$= false; }
        | NOT_SYM      { $$= true; }
        ;

opt_constraint_enforcement:
          %empty { $$= true; }
        | constraint_enforcement { $$= $1; }
        ;

constraint_enforcement:
          opt_not ENFORCED_SYM  { $$= !($1); }
        ;

old_or_new_charset_name_or_default:
          old_or_new_charset_name { $$=$1;   }
        | DEFAULT_SYM    { $$=nullptr; }
        ;

opt_default:
          %empty {}
        | DEFAULT_SYM {}
        ;

constraint_key_type:
          PRIMARY_SYM KEY_SYM { $$= KEYTYPE_PRIMARY; }
        | UNIQUE_SYM opt_key_or_index { $$= KEYTYPE_UNIQUE; }
        ;

opt_key_or_index:
          %empty {}
        | key_or_index
        ;

keys_or_index:
          KEYS {}
        | INDEX_SYM {}
        | INDEXES {}
        ;

opt_unique:
          %empty { $$= KEYTYPE_MULTIPLE; }
        | UNIQUE_SYM   { $$= KEYTYPE_UNIQUE; }
        ;

opt_fulltext_index_options:
          %empty { $$.init(YYMEM_ROOT); }
        | fulltext_index_options
        ;

fulltext_index_options:
          fulltext_index_option
          {
            $$.init(YYMEM_ROOT);
            if ($$.push_back($1))
              MYSQL_YYABORT; // OOM
          }
        | fulltext_index_options fulltext_index_option
          {
            if ($1.push_back($2))
              MYSQL_YYABORT; // OOM
            $$= $1;
          }
        ;

fulltext_index_option:
          common_index_option
        | WITH PARSER_SYM IDENT_sys
          {
            LEX_CSTRING plugin_name= {$3.str, $3.length};
            if (!plugin_is_ready(plugin_name, MYSQL_FTPARSER_PLUGIN))
            {
              my_error(ER_FUNCTION_NOT_DEFINED, MYF(0), $3.str);
              MYSQL_YYABORT;
            }
            else
              $$= NEW_PTN PT_fulltext_index_parser_name(@$, to_lex_cstring($3));
          }
        ;

opt_spatial_index_options:
          %empty { $$.init(YYMEM_ROOT); }
        | spatial_index_options
        ;

spatial_index_options:
          spatial_index_option
          {
            $$.init(YYMEM_ROOT);
            if ($$.push_back($1))
              MYSQL_YYABORT; // OOM
          }
        | spatial_index_options spatial_index_option
          {
            if ($1.push_back($2))
              MYSQL_YYABORT; // OOM
            $$= $1;
          }
        ;

spatial_index_option:
          common_index_option
        ;

opt_index_options:
          %empty { $$.init(YYMEM_ROOT); }
        | index_options
        ;

index_options:
          index_option
          {
            $$.init(YYMEM_ROOT);
            if ($$.push_back($1))
              MYSQL_YYABORT; // OOM
          }
        | index_options index_option
          {
            if ($1.push_back($2))
              MYSQL_YYABORT; // OOM
            $$= $1;
          }
        ;

index_option:
          common_index_option { $$= $1; }
        | index_type_clause { $$= $1; }
        ;

// These options are common for all index types.
common_index_option:
          KEY_BLOCK_SIZE opt_equal ulong_num { $$= NEW_PTN PT_block_size(@$, $3); }
        | COMMENT_SYM TEXT_STRING_sys
          {
            $$= NEW_PTN PT_index_comment(@$, to_lex_cstring($2));
          }
        | visibility
          {
            $$= NEW_PTN PT_index_visibility(@$, $1);
          }
        | ENGINE_ATTRIBUTE_SYM opt_equal json_attribute
          {
            $$ = make_index_engine_attribute(YYMEM_ROOT, $3);
          }
        | SECONDARY_ENGINE_ATTRIBUTE_SYM opt_equal json_attribute
          {
            $$ = make_index_secondary_engine_attribute(YYMEM_ROOT, $3);
          }
        ;

/*
  The syntax for defining an index is:

    ... INDEX [index_name] [USING|TYPE] <index_type> ...

  The problem is that whereas USING is a reserved word, TYPE is not. We can
  still handle it if an index name is supplied, i.e.:

    ... INDEX type TYPE <index_type> ...

  here the index's name is unmbiguously 'type', but for this:

    ... INDEX TYPE <index_type> ...

  it's impossible to know what this actually mean - is 'type' the name or the
  type? For this reason we accept the TYPE syntax only if a name is supplied.
*/
opt_index_name_and_type:
          opt_ident                  { $$= {$1, nullptr}; }
        | opt_ident USING index_type { $$= {$1, NEW_PTN PT_index_type(@$, $3)}; }
        | ident TYPE_SYM index_type  { $$= {$1, NEW_PTN PT_index_type(@$, $3)}; }
        ;

opt_index_type_clause:
          %empty { $$ = nullptr; }
        | index_type_clause
        ;

index_type_clause:
          USING index_type    { $$= NEW_PTN PT_index_type(@$, $2); }
        | TYPE_SYM index_type { $$= NEW_PTN PT_index_type(@$, $2); }
        ;

visibility:
          VISIBLE_SYM { $$= true; }
        | INVISIBLE_SYM { $$= false; }
        ;

index_type:
          BTREE_SYM { $$= HA_KEY_ALG_BTREE; }
        | RTREE_SYM { $$= HA_KEY_ALG_RTREE; }
        | HASH_SYM  { $$= HA_KEY_ALG_HASH; }
        ;

key_list:
          key_list ',' key_part
          {
            if ($1->push_back($3))
              MYSQL_YYABORT; // OOM
            $$= $1;
          }
        | key_part
          {
            // The order is ignored.
            $$= NEW_PTN List<PT_key_part_specification>;
            if ($$ == nullptr || $$->push_back($1))
              MYSQL_YYABORT; // OOM
          }
        ;

key_part:
          ident opt_ordering_direction
          {
            $$= NEW_PTN PT_key_part_specification(@$, to_lex_cstring($1), $2, 0);
            if ($$ == nullptr)
              MYSQL_YYABORT;
          }
        | ident '(' NUM ')' opt_ordering_direction
          {
            int key_part_length= atoi($3.str);
            if (!key_part_length)
            {
              my_error(ER_KEY_PART_0, MYF(0), $1.str);
            }
            $$= NEW_PTN PT_key_part_specification(@$, to_lex_cstring($1), $5,
                                                  key_part_length);
            if ($$ == nullptr)
              MYSQL_YYABORT; /* purecov: deadcode */
          }
        ;

key_list_with_expression:
          key_list_with_expression ',' key_part_with_expression
          {
            if ($1->push_back($3))
              MYSQL_YYABORT; /* purecov: deadcode */
            $$= $1;
          }
        | key_part_with_expression
          {
            // The order is ignored.
            $$= NEW_PTN List<PT_key_part_specification>;
            if ($$ == nullptr || $$->push_back($1))
              MYSQL_YYABORT; /* purecov: deadcode */
          }
        ;

key_part_with_expression:
          key_part
        | '(' expr ')' opt_ordering_direction
          {
            $$= NEW_PTN PT_key_part_specification(@$, $2, $4);
            if ($$ == nullptr)
              MYSQL_YYABORT;
          }
        ;

opt_ident:
          %empty { $$= NULL_STR; }
        | ident
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

alter_database_stmt:
          ALTER DATABASE ident_or_empty
          {
            Lex->create_info= YYTHD->alloc_typed<HA_CREATE_INFO>();
            if (Lex->create_info == nullptr)
              MYSQL_YYABORT; // OOM
            Lex->create_info->default_table_charset= nullptr;
            Lex->create_info->used_fields= 0;
          }
          alter_database_options
          {
            LEX *lex=Lex;
            lex->sql_command=SQLCOM_ALTER_DB;
            lex->name= $3;
            if (lex->name.str == nullptr &&
                lex->copy_db_to(&lex->name.str, &lex->name.length))
              MYSQL_YYABORT;
          }
        ;

alter_procedure_stmt:
          ALTER PROCEDURE_SYM sp_name
          {
            LEX *lex= Lex;

            if (lex->sphead)
            {
              my_error(ER_SP_NO_DROP_SP, MYF(0), "PROCEDURE");
              MYSQL_YYABORT;
            }
            memset(&lex->sp_chistics, 0, sizeof(st_sp_chistics));
          }
          sp_a_chistics
          {
            LEX *lex=Lex;

            lex->sql_command= SQLCOM_ALTER_PROCEDURE;
            lex->spname= $3;
            MAKE_CMD_DDL_DUMMY();
          }
        ;

alter_function_stmt:
          ALTER FUNCTION_SYM sp_name
          {
            LEX *lex= Lex;

            if (lex->sphead)
            {
              my_error(ER_SP_NO_DROP_SP, MYF(0), "FUNCTION");
              MYSQL_YYABORT;
            }
            memset(&lex->sp_chistics, 0, sizeof(st_sp_chistics));
          }
          sp_a_chistics
          {
            LEX *lex=Lex;

            lex->sql_command= SQLCOM_ALTER_FUNCTION;
            lex->spname= $3;
            MAKE_CMD_DDL_DUMMY();
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

alter_resource_group_stmt:
          ALTER RESOURCE_SYM GROUP_SYM ident opt_resource_group_vcpu_list
          opt_resource_group_priority opt_resource_group_enable_disable
          opt_force
          {
            $$= NEW_PTN PT_alter_resource_group(@$, to_lex_cstring($4),
                                                $5, $6, $7, $8);
          }
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

opt_ev_rename_to:
          %empty { $$= 0;}
        | RENAME TO_SYM sp_name
          {
            /*
              Use lex's spname to hold the new name.
              The original name is in the Event_parse_data object
            */
            Lex->spname= $3;
            $$= 1;
          }
        ;

opt_ev_sql_stmt:
          %empty { $$= 0;}
        | DO_SYM ev_sql_stmt { $$= 1; }
        ;

ident_or_empty:
          %empty { $$.str= nullptr; $$.length= 0; }
        | ident { $$= $1; }
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

opt_with_validation:
          %empty { $$= Alter_info::ALTER_VALIDATION_DEFAULT; }
        | with_validation
        ;

with_validation:
          WITH VALIDATION_SYM
          {
            $$= Alter_info::ALTER_WITH_VALIDATION;
          }
        | WITHOUT_SYM VALIDATION_SYM
          {
            $$= Alter_info::ALTER_WITHOUT_VALIDATION;
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

alter_commands_modifier_list:
          alter_commands_modifier
        | alter_commands_modifier_list ',' alter_commands_modifier
          {
            $$= $1;
            $$.merge($3);
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

alter_commands_modifier:
          alter_algorithm_option
          {
            $$.init();
            $$.algo.set($1);
          }
        | alter_lock_option
          {
            $$.init();
            $$.lock.set($1);
          }
        | with_validation
          {
            $$.init();
            $$.validation.set($1);
          }
        ;

opt_index_lock_and_algorithm:
          %empty { $$.init(); }
        | alter_lock_option
          {
            $$.init();
            $$.lock.set($1);
          }
        | alter_algorithm_option
          {
            $$.init();
            $$.algo.set($1);
          }
        | alter_lock_option alter_algorithm_option
          {
            $$.init();
            $$.lock.set($1);
            $$.algo.set($2);
          }
        | alter_algorithm_option alter_lock_option
          {
            $$.init();
            $$.algo.set($1);
            $$.lock.set($2);
          }
        ;

alter_algorithm_option:
          ALGORITHM_SYM opt_equal alter_algorithm_option_value { $$= $3; }
        ;

alter_algorithm_option_value:
          DEFAULT_SYM
          {
            $$= Alter_info::ALTER_TABLE_ALGORITHM_DEFAULT;
          }
        | ident
          {
            if (is_identifier($1, "INPLACE"))
              $$= Alter_info::ALTER_TABLE_ALGORITHM_INPLACE;
            else if (is_identifier($1, "INSTANT"))
              $$= Alter_info::ALTER_TABLE_ALGORITHM_INSTANT;
            else if (is_identifier($1, "COPY"))
              $$= Alter_info::ALTER_TABLE_ALGORITHM_COPY;
            else
            {
              my_error(ER_UNKNOWN_ALTER_ALGORITHM, MYF(0), $1.str);
              MYSQL_YYABORT;
            }
          }
        ;

alter_lock_option:
          LOCK_SYM opt_equal alter_lock_option_value { $$= $3; }
        ;

alter_lock_option_value:
          DEFAULT_SYM
          {
            $$= Alter_info::ALTER_TABLE_LOCK_DEFAULT;
          }
        | ident
          {
            if (is_identifier($1, "NONE"))
              $$= Alter_info::ALTER_TABLE_LOCK_NONE;
            else if (is_identifier($1, "SHARED"))
              $$= Alter_info::ALTER_TABLE_LOCK_SHARED;
            else if (is_identifier($1, "EXCLUSIVE"))
              $$= Alter_info::ALTER_TABLE_LOCK_EXCLUSIVE;
            else
            {
              my_error(ER_UNKNOWN_ALTER_LOCK, MYF(0), $1.str);
              MYSQL_YYABORT;
            }
          }
        ;

opt_column:
          %empty
        | COLUMN_SYM
        ;

opt_restrict:
          %empty      { $$= DROP_DEFAULT; }
        | RESTRICT    { $$= DROP_RESTRICT; }
        | CASCADE     { $$= DROP_CASCADE; }
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

replica:
        SLAVE { Lex->set_replication_deprecated_syntax_used(); }
      | REPLICA_SYM
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

start:
          START_SYM TRANSACTION_SYM opt_start_transaction_option_list
          {
            LEX *lex= Lex;
            lex->sql_command= SQLCOM_BEGIN;
            /* READ ONLY and READ WRITE are mutually exclusive. */
            if (($3 & MYSQL_START_TRANS_OPT_READ_WRITE) &&
                ($3 & MYSQL_START_TRANS_OPT_READ_ONLY))
            {
              YYTHD->syntax_error();
              MYSQL_YYABORT;
            }
            lex->start_transaction_opt= $3;
          }
        ;

opt_start_transaction_option_list:
          %empty
          {
            $$= 0;
          }
        | start_transaction_option_list
          {
            $$= $1;
          }
        ;

start_transaction_option_list:
          start_transaction_option
          {
            $$= $1;
          }
        | start_transaction_option_list ',' start_transaction_option
          {
            $$= $1 | $3;
          }
        ;

start_transaction_option:
          WITH CONSISTENT_SYM SNAPSHOT_SYM
          {
            $$= MYSQL_START_TRANS_OPT_WITH_CONS_SNAPSHOT;
          }
        | READ_SYM ONLY_SYM
          {
            $$= MYSQL_START_TRANS_OPT_READ_ONLY;
          }
        | READ_SYM WRITE_SYM
          {
            $$= MYSQL_START_TRANS_OPT_READ_WRITE;
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

checksum:
          CHECKSUM_SYM table_or_tables table_list opt_checksum_type
          {
            LEX *lex=Lex;
            lex->sql_command = SQLCOM_CHECKSUM;
            /* Will be overriden during execution. */
            YYPS->m_lock_type= TL_UNLOCK;
            if (Select->add_tables(YYTHD, $3, TL_OPTION_UPDATING,
                                   YYPS->m_lock_type, YYPS->m_mdl_type))
              MYSQL_YYABORT;
            Lex->check_opt.flags= $4;
          }
        ;

opt_checksum_type:
          %empty        { $$= 0; }
        | QUICK         { $$= T_QUICK; }
        | EXTENDED_SYM  { $$= T_EXTEND; }
        ;

repair_table_stmt:
          REPAIR opt_no_write_to_binlog table_or_tables
          table_list opt_mi_repair_types
          {
            $$= NEW_PTN PT_repair_table_stmt(@$, YYMEM_ROOT, $2, $4,
                                             $5.flags, $5.sql_flags);
          }
        ;

opt_mi_repair_types:
          %empty { $$.flags = T_MEDIUM; $$.sql_flags= 0; }
        | mi_repair_types
        ;

mi_repair_types:
          mi_repair_type
        | mi_repair_types mi_repair_type
          {
            $$.flags= $1.flags | $2.flags;
            $$.sql_flags= $1.sql_flags | $2.sql_flags;
          }
        ;

mi_repair_type:
          QUICK        { $$.flags= T_QUICK;  $$.sql_flags= 0; }
        | EXTENDED_SYM { $$.flags= T_EXTEND; $$.sql_flags= 0; }
        | USE_FRM      { $$.flags= 0;        $$.sql_flags= TT_USEFRM; }
        ;

analyze_table_stmt:
          ANALYZE_SYM opt_no_write_to_binlog table_or_tables table_list
          opt_histogram
          {
            if ($5.param) {
              $$= NEW_PTN PT_analyze_table_stmt(@$, YYMEM_ROOT, $2, $4,
                                                $5.command, $5.param->num_buckets,
                                                $5.columns, $5.param->data);
            } else {
              $$= NEW_PTN PT_analyze_table_stmt(@$, YYMEM_ROOT, $2, $4,
                                                $5.command, 0,
                                                $5.columns, {nullptr, 0});
            }
          }
        ;

opt_histogram_update_param:
          %empty
          {
            $$.num_buckets= DEFAULT_NUMBER_OF_HISTOGRAM_BUCKETS;
            $$.data= { nullptr, 0 };
          }
        | WITH NUM BUCKETS_SYM
          {
            int error;
            longlong num= my_strtoll10($2.str, nullptr, &error);
            MYSQL_YYABORT_UNLESS(error <= 0);

            if (num < 1 || num > MAX_NUMBER_OF_HISTOGRAM_BUCKETS)
            {
              my_error(ER_DATA_OUT_OF_RANGE, MYF(0), "Number of buckets",
                       "ANALYZE TABLE");
              MYSQL_YYABORT;
            }

            $$.num_buckets= num;
            $$.data= { nullptr, 0 };
          }
        | USING DATA_SYM TEXT_STRING_literal
          {
            $$.num_buckets= 0;
            $$.data= $3;
          }
        ;

opt_histogram:
          %empty
          {
            $$.command= Sql_cmd_analyze_table::Histogram_command::NONE;
            $$.columns= nullptr;
            $$.param= nullptr;
          }
        | UPDATE_SYM HISTOGRAM_SYM ON_SYM ident_string_list opt_histogram_update_param
          {
            $$.command=
              Sql_cmd_analyze_table::Histogram_command::UPDATE_HISTOGRAM;
            $$.columns= $4;
            $$.param= NEW_PTN YYSTYPE::Histogram_param($5);
            if ($$.param == nullptr)
              MYSQL_YYABORT; // OOM
          }
        | DROP HISTOGRAM_SYM ON_SYM ident_string_list
          {
            $$.command=
              Sql_cmd_analyze_table::Histogram_command::DROP_HISTOGRAM;
            $$.columns= $4;
            $$.param = nullptr;
          }
        ;

binlog_base64_event:
          BINLOG_SYM TEXT_STRING_sys
          {
            Lex->sql_command = SQLCOM_BINLOG_BASE64_EVENT;
            Lex->binlog_stmt_arg= $2;
          }
        ;

check_table_stmt:
          CHECK_SYM table_or_tables table_list opt_mi_check_types
          {
            $$= NEW_PTN PT_check_table_stmt(@$, YYMEM_ROOT, $3,
                                            $4.flags, $4.sql_flags);
          }
        ;

opt_mi_check_types:
          %empty { $$.flags = T_MEDIUM; $$.sql_flags= 0; }
        | mi_check_types
        ;

mi_check_types:
          mi_check_type
        | mi_check_type mi_check_types
          {
            $$.flags= $1.flags | $2.flags;
            $$.sql_flags= $1.sql_flags | $2.sql_flags;
          }
        ;

mi_check_type:
          QUICK
          { $$.flags= T_QUICK;              $$.sql_flags= 0; }
        | FAST_SYM
          { $$.flags= T_FAST;               $$.sql_flags= 0; }
        | MEDIUM_SYM
          { $$.flags= T_MEDIUM;             $$.sql_flags= 0; }
        | EXTENDED_SYM
          { $$.flags= T_EXTEND;             $$.sql_flags= 0; }
        | CHANGED
          { $$.flags= T_CHECK_ONLY_CHANGED; $$.sql_flags= 0; }
        | FOR_SYM UPGRADE_SYM
          { $$.flags= 0;                    $$.sql_flags= TT_FOR_UPGRADE; }
        ;

optimize_table_stmt:
          OPTIMIZE opt_no_write_to_binlog table_or_tables table_list
          {
            $$= NEW_PTN PT_optimize_table_stmt(@$, YYMEM_ROOT, $2, $4);
          }
        ;

opt_no_write_to_binlog:
          %empty { $$= 0; }
        | NO_WRITE_TO_BINLOG { $$= 1; }
        | LOCAL_SYM { $$= 1; }
        ;

rename:
          RENAME table_or_tables
          {
            Lex->sql_command= SQLCOM_RENAME_TABLE;
          }
          table_to_table_list
          {}
        | RENAME USER rename_list
          {
            Lex->sql_command = SQLCOM_RENAME_USER;
          }
        ;

rename_list:
          user TO_SYM user
          {
            if (Lex->users_list.push_back($1) || Lex->users_list.push_back($3))
              MYSQL_YYABORT;
          }
        | rename_list ',' user TO_SYM user
          {
            if (Lex->users_list.push_back($3) || Lex->users_list.push_back($5))
              MYSQL_YYABORT;
          }
        ;

table_to_table_list:
          table_to_table
        | table_to_table_list ',' table_to_table
        ;

table_to_table:
          table_ident TO_SYM table_ident
          {
            LEX *lex=Lex;
            Query_block *sl= Select;
            if (!sl->add_table_to_list(lex->thd, $1,nullptr,TL_OPTION_UPDATING,
                                       TL_IGNORE, MDL_EXCLUSIVE) ||
                !sl->add_table_to_list(lex->thd, $3,nullptr,TL_OPTION_UPDATING,
                                       TL_IGNORE, MDL_EXCLUSIVE))
              MYSQL_YYABORT;
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

/*
  DO statement
*/

do_stmt:
          DO_SYM select_item_list
          {
            $$= NEW_PTN PT_select_stmt(@$, SQLCOM_DO,
                  NEW_PTN PT_query_expression(@$,
                    NEW_PTN PT_query_specification(@$, {}, $2)));
          }
        ;

/*
  Drop : delete tables or index or user or role
*/

drop_table_stmt:
          DROP opt_temporary table_or_tables if_exists table_list opt_restrict
          {
            // Note: opt_restrict ($6) is ignored!
            LEX *lex=Lex;
            lex->sql_command = SQLCOM_DROP_TABLE;
            lex->drop_temporary= $2;
            lex->drop_if_exists= $4;
            YYPS->m_lock_type= TL_UNLOCK;
            YYPS->m_mdl_type= MDL_EXCLUSIVE;
            if (Select->add_tables(YYTHD, $5, TL_OPTION_UPDATING,
                                   YYPS->m_lock_type, YYPS->m_mdl_type))
              MYSQL_YYABORT;

            Lex->m_sql_cmd= NEW_PTN Sql_cmd_drop_table();
            if (!Lex->m_sql_cmd)
              MYSQL_YYABORT; /* purecov: inspected */ //OOM
          }
        ;

drop_index_stmt:
          DROP INDEX_SYM ident ON_SYM table_ident opt_index_lock_and_algorithm
          {
            $$= NEW_PTN PT_drop_index_stmt(@$, YYMEM_ROOT, $3.str, $5,
                                           $6.algo.get_or_default(),
                                           $6.lock.get_or_default());
          }
        ;

drop_database_stmt:
          DROP DATABASE if_exists ident
          {
            LEX *lex=Lex;
            lex->sql_command= SQLCOM_DROP_DB;
            lex->drop_if_exists=$3;
            lex->name= $4;
            MAKE_CMD_DDL_DUMMY();
          }
        ;

drop_function_stmt:
          DROP FUNCTION_SYM if_exists ident '.' ident
          {
            THD *thd= YYTHD;
            LEX *lex= thd->lex;
            sp_name *spname;
            if ($4.str &&
                (check_and_convert_db_name(&$4, false) != Ident_name_check::OK))
               MYSQL_YYABORT;
            if (sp_check_name(&$6))
               MYSQL_YYABORT;
            if (lex->sphead)
            {
              my_error(ER_SP_NO_DROP_SP, MYF(0), "FUNCTION");
              MYSQL_YYABORT;
            }
            lex->sql_command = SQLCOM_DROP_FUNCTION;
            lex->drop_if_exists= $3;
            spname= new (YYMEM_ROOT) sp_name(to_lex_cstring($4), $6, true);
            if (spname == nullptr)
              MYSQL_YYABORT;
            spname->init_qname(thd);
            lex->spname= spname;
            MAKE_CMD_DDL_DUMMY();
          }
        | DROP FUNCTION_SYM if_exists ident
          {
            /*
              Unlike DROP PROCEDURE, "DROP FUNCTION ident" should work
              even if there is no current database. In this case it
              applies only to UDF.
              Hence we can't merge rules for "DROP FUNCTION ident.ident"
              and "DROP FUNCTION ident" into one "DROP FUNCTION sp_name"
              rule. sp_name assumes that database name should be always
              provided - either explicitly or implicitly.
            */
            THD *thd= YYTHD;
            LEX *lex= thd->lex;
            LEX_STRING db= NULL_STR;
            sp_name *spname;
            if (lex->sphead)
            {
              my_error(ER_SP_NO_DROP_SP, MYF(0), "FUNCTION");
              MYSQL_YYABORT;
            }
            if (thd->db().str && lex->copy_db_to(&db.str, &db.length))
              MYSQL_YYABORT;
            if (sp_check_name(&$4))
               MYSQL_YYABORT;
            lex->sql_command = SQLCOM_DROP_FUNCTION;
            lex->drop_if_exists= $3;
            spname= new (YYMEM_ROOT) sp_name(to_lex_cstring(db), $4, false);
            if (spname == nullptr)
              MYSQL_YYABORT;
            spname->init_qname(thd);
            lex->spname= spname;
            MAKE_CMD_DDL_DUMMY();
          }
        ;

drop_resource_group_stmt:
          DROP RESOURCE_SYM GROUP_SYM ident opt_force
          {
            $$= NEW_PTN PT_drop_resource_group(@$, to_lex_cstring($4), $5);
          }
         ;

drop_procedure_stmt:
          DROP PROCEDURE_SYM if_exists sp_name
          {
            LEX *lex=Lex;
            if (lex->sphead)
            {
              my_error(ER_SP_NO_DROP_SP, MYF(0), "PROCEDURE");
              MYSQL_YYABORT;
            }
            lex->sql_command = SQLCOM_DROP_PROCEDURE;
            lex->drop_if_exists= $3;
            lex->spname= $4;
            MAKE_CMD_DDL_DUMMY();
          }
        ;

drop_user_stmt:
          DROP USER if_exists user_list
          {
             LEX *lex=Lex;
             lex->sql_command= SQLCOM_DROP_USER;
             lex->drop_if_exists= $3;
             lex->users_list= *$4;
             MAKE_CMD_DCL_DUMMY();
          }
        ;

drop_view_stmt:
          DROP VIEW_SYM if_exists table_list opt_restrict
          {
            // Note: opt_restrict ($5) is ignored!
            LEX *lex= Lex;
            lex->sql_command= SQLCOM_DROP_VIEW;
            lex->drop_if_exists= $3;
            YYPS->m_lock_type= TL_UNLOCK;
            YYPS->m_mdl_type= MDL_EXCLUSIVE;
            if (Select->add_tables(YYTHD, $4, TL_OPTION_UPDATING,
                                   YYPS->m_lock_type, YYPS->m_mdl_type))
              MYSQL_YYABORT;
            MAKE_CMD_DDL_DUMMY();
          }
        ;

drop_event_stmt:
          DROP EVENT_SYM if_exists sp_name
          {
            Lex->drop_if_exists= $3;
            Lex->spname= $4;
            Lex->sql_command = SQLCOM_DROP_EVENT;
            MAKE_CMD_DDL_DUMMY();
          }
        ;

drop_trigger_stmt:
          DROP TRIGGER_SYM if_exists sp_name
          {
            LEX *lex= Lex;
            lex->sql_command= SQLCOM_DROP_TRIGGER;
            lex->drop_if_exists= $3;
            lex->spname= $4;
            Lex->m_sql_cmd= new (YYTHD->mem_root) Sql_cmd_drop_trigger();
          }
        ;

drop_tablespace_stmt:
          DROP TABLESPACE_SYM ident opt_drop_ts_options
          {
            auto pc= NEW_PTN Alter_tablespace_parse_context{YYTHD};
            if (pc == nullptr)
              MYSQL_YYABORT; /* purecov: inspected */ // OOM

            if ($4 != nullptr)
            {
              if (YYTHD->is_error() || contextualize_array(pc, $4))
                MYSQL_YYABORT; /* purecov: inspected */
            }

            auto cmd= NEW_PTN Sql_cmd_drop_tablespace{$3, pc};
            if (!cmd)
              MYSQL_YYABORT; /* purecov: inspected */ // OOM
            Lex->m_sql_cmd= cmd;
            Lex->sql_command= SQLCOM_ALTER_TABLESPACE;
          }

drop_undo_tablespace_stmt:
          DROP UNDO_SYM TABLESPACE_SYM ident opt_undo_tablespace_options
          {
            auto pc= NEW_PTN Alter_tablespace_parse_context{YYTHD};
            if (pc == nullptr)
              MYSQL_YYABORT; // OOM

            if ($5 != nullptr)
            {
              if (YYTHD->is_error() || contextualize_array(pc, $5))
                MYSQL_YYABORT;
            }

            auto cmd= NEW_PTN Sql_cmd_drop_undo_tablespace{
              DROP_UNDO_TABLESPACE, $4, {nullptr, 0},  pc};
            if (!cmd)
              MYSQL_YYABORT; // OOM
            Lex->m_sql_cmd= cmd;
            Lex->sql_command= SQLCOM_ALTER_TABLESPACE;
          }
        ;

drop_logfile_stmt:
          DROP LOGFILE_SYM GROUP_SYM ident opt_drop_ts_options
          {
            auto pc= NEW_PTN Alter_tablespace_parse_context{YYTHD};
            if (pc == nullptr)
              MYSQL_YYABORT; /* purecov: inspected */ // OOM

            if ($5 != nullptr)
            {
              if (YYTHD->is_error() || contextualize_array(pc, $5))
                MYSQL_YYABORT; /* purecov: inspected */
            }

            auto cmd= NEW_PTN Sql_cmd_logfile_group{DROP_LOGFILE_GROUP,
                                                    $4, pc};
            if (!cmd)
              MYSQL_YYABORT; /* purecov: inspected */ // OOM
            Lex->m_sql_cmd= cmd;
            Lex->sql_command= SQLCOM_ALTER_TABLESPACE;
          }

        ;

drop_server_stmt:
          DROP SERVER_SYM if_exists ident_or_text
          {
            Lex->sql_command = SQLCOM_DROP_SERVER;
            Lex->m_sql_cmd= NEW_PTN Sql_cmd_drop_server($4, $3);
          }
        ;

drop_srs_stmt:
          DROP SPATIAL_SYM REFERENCE_SYM SYSTEM_SYM if_exists real_ulonglong_num
          {
            $$= NEW_PTN PT_drop_srs(@$, $6, $5);
          }
        ;

drop_role_stmt:
          DROP ROLE_SYM if_exists role_list
          {
            $$= NEW_PTN PT_drop_role(@$, $3, $4);
          }
        ;

table_list:
          table_ident
          {
            $$= NEW_PTN Mem_root_array<Table_ident *>(YYMEM_ROOT);
            if ($$->push_back($1))
              MYSQL_YYABORT; // OOM
          }
        | table_list ',' table_ident
          {
            $$= $1;
            if ($$ == nullptr || $$->push_back($3))
              MYSQL_YYABORT; // OOM
          }
        ;

if_exists:
          %empty { $$= 0; }
        | IF EXISTS { $$= 1; }
        ;

opt_ignore_unknown_user:
          %empty { $$= 0; }
        | IGNORE_SYM UNKNOWN_SYM USER { $$= 1; }
        ;

opt_temporary:
          %empty { $$= false; }
        | TEMPORARY   { $$= true; }
        ;

opt_drop_ts_options:
        %empty { $$= nullptr; }
      | drop_ts_option_list
      ;

drop_ts_option_list:
          drop_ts_option
          {
            $$= NEW_PTN Mem_root_array<PT_alter_tablespace_option_base*>(YYMEM_ROOT);
            if ($$ == nullptr || $$->push_back($1))
              MYSQL_YYABORT; /* purecov: inspected */ // OOM
          }
        | drop_ts_option_list opt_comma drop_ts_option
          {
            $$= $1;
            if ($$->push_back($3))
              MYSQL_YYABORT; /* purecov: inspected */ // OOM
          }
        ;

drop_ts_option:
          ts_option_engine
        | ts_option_wait
        ;

truncate_stmt:
          TRUNCATE_SYM opt_table table_ident
          {
            $$= NEW_PTN PT_truncate_table_stmt(@$, $3);
          }
        ;

opt_table:
          %empty
        | TABLE_SYM
        ;

opt_profile_defs:
          %empty { $$ = 0; }
        | profile_defs
        ;

profile_defs:
          profile_def
        | profile_defs ',' profile_def  { $$ = $1 | $3; }
        ;

profile_def:
          CPU_SYM                   { $$ = PROFILE_CPU; }
        | MEMORY_SYM                { $$ = PROFILE_MEMORY; }
        | BLOCK_SYM IO_SYM          { $$ = PROFILE_BLOCK_IO; }
        | CONTEXT_SYM SWITCHES_SYM  { $$ = PROFILE_CONTEXT; }
        | PAGE_SYM FAULTS_SYM       { $$ = PROFILE_PAGE_FAULTS; }
        | IPC_SYM                   { $$ = PROFILE_IPC; }
        | SWAPS_SYM                 { $$ = PROFILE_SWAPS; }
        | SOURCE_SYM                { $$ = PROFILE_SOURCE; }
        | ALL                       { $$ = PROFILE_ALL; }
        ;

opt_for_query:
          %empty { $$ = 0; }
        | FOR_SYM QUERY_SYM NUM
          {
            int error;
            $$ = static_cast<my_thread_id>(my_strtoll10($3.str, nullptr, &error));
            if (error != 0)
              MYSQL_YYABORT;
          }
        ;

/* SHOW statements */

show_databases_stmt:
           SHOW DATABASES opt_wild_or_where
           {
             $$ = NEW_PTN PT_show_databases(@$, $3.wild, $3.where);
           }

show_tables_stmt:
          SHOW opt_show_cmd_type TABLES opt_db opt_wild_or_where
          {
            $$ = NEW_PTN PT_show_tables(@$, $2, $4, $5.wild, $5.where);
          }
        ;

show_triggers_stmt:
          SHOW opt_full TRIGGERS_SYM opt_db opt_wild_or_where
          {
            $$ = NEW_PTN PT_show_triggers(@$, $2, $4, $5.wild, $5.where);
          }
        ;

show_events_stmt:
          SHOW EVENTS_SYM opt_db opt_wild_or_where
          {
            $$ = NEW_PTN PT_show_events(@$, $3, $4.wild, $4.where);
          }
        ;

show_table_status_stmt:
          SHOW TABLE_SYM STATUS_SYM opt_db opt_wild_or_where
          {
            $$ = NEW_PTN PT_show_table_status(@$, $4, $5.wild, $5.where);
          }
        ;

show_open_tables_stmt:
          SHOW OPEN_SYM TABLES opt_db opt_wild_or_where
          {
             $$ = NEW_PTN PT_show_open_tables(@$, $4, $5.wild, $5.where);
          }
        ;

show_plugins_stmt:
          SHOW PLUGINS_SYM
          {
            $$ = NEW_PTN PT_show_plugins(@$);
          }
        ;

show_engine_logs_stmt:
          SHOW ENGINE_SYM engine_or_all LOGS_SYM
          {
            $$ = NEW_PTN PT_show_engine_logs(@$, $3);
          }
        ;

show_engine_mutex_stmt:
          SHOW ENGINE_SYM engine_or_all MUTEX_SYM
          {
            $$ = NEW_PTN PT_show_engine_mutex(@$, $3);
          }
        ;

show_engine_status_stmt:
          SHOW ENGINE_SYM engine_or_all STATUS_SYM
          {
            $$ = NEW_PTN PT_show_engine_status(@$, $3);
          }
        ;

show_columns_stmt:
          SHOW                  /* 1 */
          opt_show_cmd_type     /* 2 */
          COLUMNS               /* 3 */
          from_or_in            /* 4 */
          table_ident           /* 5 */
          opt_db                /* 6 */
          opt_wild_or_where     /* 7 */
          {
            if ($6)
              $5->change_db($6);

            $$ = NEW_PTN PT_show_fields(@$, $2, $5, $7.wild, $7.where);
          }
        ;

show_binary_logs_stmt:
          SHOW master_or_binary LOGS_SYM
          {
            if (Lex->is_replication_deprecated_syntax_used())
            {
              push_deprecated_warn(YYTHD, "SHOW MASTER LOGS", "SHOW BINARY LOGS");
            }
            $$ = NEW_PTN PT_show_binlogs(@$);
          }
        ;

show_replicas_stmt:
          SHOW SLAVE HOSTS_SYM
          {
            Lex->set_replication_deprecated_syntax_used();
            push_deprecated_warn(YYTHD, "SHOW SLAVE HOSTS", "SHOW REPLICAS");

            $$ = NEW_PTN PT_show_replicas(@$);
          }
        | SHOW REPLICAS_SYM
          {
            $$ = NEW_PTN PT_show_replicas(@$);
          }
        ;

show_binlog_events_stmt:
          SHOW BINLOG_SYM EVENTS_SYM opt_binlog_in binlog_from opt_limit_clause
          {
            $$ = NEW_PTN PT_show_binlog_events(@$, $4, $6);
          }
        ;

show_relaylog_events_stmt:
          SHOW RELAYLOG_SYM EVENTS_SYM opt_binlog_in binlog_from opt_limit_clause
          opt_channel
          {
            $$ = NEW_PTN PT_show_relaylog_events(@$, $4, $6, $7);
          }
        ;

show_keys_stmt:
          SHOW                  /* #1 */
          opt_extended          /* #2 */
          keys_or_index         /* #3 */
          from_or_in            /* #4 */
          table_ident           /* #5 */
          opt_db                /* #6 */
          opt_where_clause      /* #7 */
          {
            if ($6)
              $5->change_db($6);

            $$ = NEW_PTN PT_show_keys(@$, $2, $5, $7);
          }
        ;

show_engines_stmt:
          SHOW opt_storage ENGINES_SYM
          {
            $$ = NEW_PTN PT_show_engines(@$);
          }
        ;

show_count_warnings_stmt:
          SHOW COUNT_SYM '(' '*' ')' WARNINGS
          {
            $$ = NEW_PTN PT_show_count_warnings(@$);
          }
        ;

show_count_errors_stmt:
          SHOW COUNT_SYM '(' '*' ')' ERRORS
          {
            $$ = NEW_PTN PT_show_count_errors(@$);
          }
        ;

show_warnings_stmt:
          SHOW WARNINGS opt_limit_clause
          {
            $$ = NEW_PTN PT_show_warnings(@$, $3);
          }
        ;

show_errors_stmt:
          SHOW ERRORS opt_limit_clause
          {
            $$ = NEW_PTN PT_show_errors(@$, $3);
          }
        ;

show_profiles_stmt:
          SHOW PROFILES_SYM
          {
            push_warning_printf(YYTHD, Sql_condition::SL_WARNING,
                                ER_WARN_DEPRECATED_SYNTAX,
                                ER_THD(YYTHD, ER_WARN_DEPRECATED_SYNTAX),
                                "SHOW PROFILES", "Performance Schema");
            $$ = NEW_PTN PT_show_profiles(@$);
          }
        ;

show_profile_stmt:
          SHOW PROFILE_SYM opt_profile_defs opt_for_query opt_limit_clause
          {
            $$ = NEW_PTN PT_show_profile(@$, $3, $4, $5);
          }
        ;

show_status_stmt:
          SHOW opt_var_type STATUS_SYM opt_wild_or_where
          {
             $$ = NEW_PTN PT_show_status(@$, $2, $4.wild, $4.where);
          }
        ;

show_processlist_stmt:
          SHOW opt_full PROCESSLIST_SYM
          {
            $$ = NEW_PTN PT_show_processlist(@$, $2);
          }
        ;

show_variables_stmt:
          SHOW opt_var_type VARIABLES opt_wild_or_where
          {
            $$ = NEW_PTN PT_show_variables(@$, $2, $4.wild, $4.where);
          }
        ;

show_character_set_stmt:
          SHOW character_set opt_wild_or_where
          {
            $$ = NEW_PTN PT_show_charsets(@$, $3.wild, $3.where);
          }
        ;

show_collation_stmt:
          SHOW COLLATION_SYM opt_wild_or_where
          {
            $$ = NEW_PTN PT_show_collations(@$, $3.wild, $3.where);
          }
        ;

show_privileges_stmt:
          SHOW PRIVILEGES
          {
            $$ = NEW_PTN PT_show_privileges(@$);
          }
        ;

show_grants_stmt:
          SHOW GRANTS
          {
            $$ = NEW_PTN PT_show_grants(@$, nullptr, nullptr);
          }
        | SHOW GRANTS FOR_SYM user
          {
            $$ = NEW_PTN PT_show_grants(@$, $4, nullptr);
          }
        | SHOW GRANTS FOR_SYM user USING user_list
          {
            $$ = NEW_PTN PT_show_grants(@$, $4, $6);
          }
        ;

show_create_database_stmt:
          SHOW CREATE DATABASE opt_if_not_exists ident
          {
            $$ = NEW_PTN PT_show_create_database(@$, $4, $5);
          }
        ;

show_create_table_stmt:
          SHOW CREATE TABLE_SYM table_ident
          {
            $$ = NEW_PTN PT_show_create_table(@$, $4);
          }
        ;

show_create_view_stmt:
          SHOW CREATE VIEW_SYM table_ident
          {
            $$ = NEW_PTN PT_show_create_view(@$, $4);
          }
        ;

show_master_status_stmt:
          SHOW MASTER_SYM STATUS_SYM
          {
            push_deprecated_warn(YYTHD, "SHOW MASTER STATUS", "SHOW BINARY LOG STATUS");
            $$ = NEW_PTN PT_show_binary_log_status(@$);
          }
        ;

show_binary_log_status_stmt:
          SHOW BINARY_SYM LOG_SYM STATUS_SYM
          {
            $$ = NEW_PTN PT_show_binary_log_status(@$);
          }
        ;

show_replica_status_stmt:
          SHOW replica STATUS_SYM opt_channel
          {
            if (Lex->is_replication_deprecated_syntax_used())
              push_deprecated_warn(YYTHD, "SHOW SLAVE STATUS", "SHOW REPLICA STATUS");
            $$ = NEW_PTN PT_show_replica_status(@$, $4);
          }
        ;

show_create_procedure_stmt:
          SHOW CREATE PROCEDURE_SYM sp_name
          {
            $$ = NEW_PTN PT_show_create_procedure(@$, $4);
          }
        ;

show_create_function_stmt:
          SHOW CREATE FUNCTION_SYM sp_name
          {
            $$ = NEW_PTN PT_show_create_function(@$, $4);
          }
        ;

show_create_trigger_stmt:
          SHOW CREATE TRIGGER_SYM sp_name
          {
            $$ = NEW_PTN PT_show_create_trigger(@$, $4);
          }
        ;

show_procedure_status_stmt:
          SHOW PROCEDURE_SYM STATUS_SYM opt_wild_or_where
          {
            $$ = NEW_PTN PT_show_status_proc(@$, $4.wild, $4.where);
          }
        ;

show_function_status_stmt:
          SHOW FUNCTION_SYM STATUS_SYM opt_wild_or_where
          {
            $$ = NEW_PTN PT_show_status_func(@$, $4.wild, $4.where);
          }
        ;

show_procedure_code_stmt:
          SHOW PROCEDURE_SYM CODE_SYM sp_name
          {
            $$ = NEW_PTN PT_show_procedure_code(@$, $4);
          }
        ;

show_function_code_stmt:
          SHOW FUNCTION_SYM CODE_SYM sp_name
          {
            $$ = NEW_PTN PT_show_function_code(@$, $4);
          }
        ;

show_create_event_stmt:
          SHOW CREATE EVENT_SYM sp_name
          {
            $$ = NEW_PTN PT_show_create_event(@$, $4);
          }
        ;

show_create_user_stmt:
          SHOW CREATE USER user
          {
            $$ = NEW_PTN PT_show_create_user(@$, $4);
          }
        ;

show_parse_tree_stmt:
          SHOW PARSE_TREE_SYM simple_statement
          {
#ifndef WITH_SHOW_PARSE_TREE
            YYTHD->syntax_error_at(@2);
            MYSQL_YYABORT;
#endif
            $$ = NEW_PTN PT_show_parse_tree(@$, $3);
          }
        ;

engine_or_all:
          ident_or_text
        | ALL           { $$ = {}; }
        ;

master_or_binary:
          MASTER_SYM
          {
            Lex->set_replication_deprecated_syntax_used();
          }
        | BINARY_SYM
        ;

master_or_binary_logs_and_gtids:
          MASTER_SYM
          {
            Lex->set_replication_deprecated_syntax_used();
          }
        | BINARY_SYM LOGS_SYM AND_SYM GTIDS_SYM
        ;

opt_storage:
          %empty
        | STORAGE_SYM
        ;

opt_db:
          %empty { $$= nullptr; }
        | from_or_in ident { $$= $2.str; }
        ;

opt_full:
          %empty      { $$= 0; }
        | FULL        { $$= 1; }
        ;

opt_extended:
          %empty        { $$= 0; }
        | EXTENDED_SYM  { $$= 1; }
        ;

opt_show_cmd_type:
          %empty               { $$= Show_cmd_type::STANDARD; }
        | FULL                 { $$= Show_cmd_type::FULL_SHOW; }
        | EXTENDED_SYM         { $$= Show_cmd_type::EXTENDED_SHOW; }
        | EXTENDED_SYM FULL    { $$= Show_cmd_type::EXTENDED_FULL_SHOW; }
        ;

from_or_in:
          FROM
        | IN_SYM
        ;

opt_binlog_in:
          %empty                 { $$ = {}; }
        | IN_SYM TEXT_STRING_sys { $$ = $2; }
        ;

binlog_from:
          %empty { Lex->mi.pos = 4; /* skip magic number */ }
        | FROM ulonglong_num { Lex->mi.pos = $2; }
        ;

opt_wild_or_where:
          %empty                        { $$ = {}; }
        | LIKE TEXT_STRING_literal      { $$ = { $2, {} }; }
        | where_clause                  { $$ = { {}, $1 }; }
        ;

/* A Oracle compatible synonym for show */
describe_stmt:
          describe_command table_ident opt_describe_column
          {
            $$= NEW_PTN PT_show_fields(@$, Show_cmd_type::STANDARD, $2, $3);
          }
        ;

explain_stmt:
          describe_command opt_explain_options explainable_stmt
          {
            $$= NEW_PTN PT_explain(@$, $2.explain_format_type, $2.is_analyze,
                  $2.is_explicit, $3.statement,
                  $2.explain_into_variable_name.length ?
                  std::optional<std::string_view>(
                    to_string_view($2.explain_into_variable_name)) :
                  std::optional<std::string_view>(std::nullopt),
                  $3.schema_name_for_explain);
          }
        ;

explainable_stmt:
          opt_explain_for_schema select_stmt
          {
            $$.statement = $2;
            $$.schema_name_for_explain = $1;
          }
        | opt_explain_for_schema insert_stmt
          {
            $$.statement = $2;
            $$.schema_name_for_explain = $1;
          }
        | opt_explain_for_schema replace_stmt
          {
            $$.statement = $2;
            $$.schema_name_for_explain = $1;
          }
        | opt_explain_for_schema update_stmt
          {
            $$.statement = $2;
            $$.schema_name_for_explain = $1;
          }
        | opt_explain_for_schema delete_stmt
          {
            $$.statement = $2;
            $$.schema_name_for_explain = $1;
          }
        | FOR_SYM CONNECTION_SYM real_ulong_num
          {
            $$.statement = NEW_PTN PT_explain_for_connection(@$, static_cast<my_thread_id>($3));
            $$.schema_name_for_explain = NULL_CSTR;
          }
        ;

describe_command:
          DESC
        | DESCRIBE
        ;

opt_explain_format:
          %empty
          {
            $$.is_explicit = false;
            $$.explain_format_type = YYTHD->variables.explain_format;
          }
        | FORMAT_SYM EQ ident_or_text
          {
            $$.is_explicit = true;
            if (is_identifier($3, "JSON"))
              $$.explain_format_type = Explain_format_type::JSON;
            else if (is_identifier($3, "TRADITIONAL"))
              $$.explain_format_type = Explain_format_type::TRADITIONAL;
            else if (is_identifier($3, "TREE"))
              $$.explain_format_type = Explain_format_type::TREE;
            else {
              // This includes even TRADITIONAL_STRICT. Since this value is
              // only meant for mtr infrastructure temporarily, we don't want
              // the user to explicitly use this value in EXPLAIN statements.
              // This results in having one less place to deprecate from.
              my_error(ER_UNKNOWN_EXPLAIN_FORMAT, MYF(0), $3.str);
              MYSQL_YYABORT;
            }
          }
        ;

opt_explain_options:
          ANALYZE_SYM opt_explain_format
          {
            $$ = $2;
            $$.is_analyze = true;
            $$.explain_into_variable_name = NULL_STR;
          }
        | opt_explain_format opt_explain_into
          {
            $$ = $1;
            $$.is_analyze = false;

            if ($2.length) {
              if (!$$.is_explicit) {
                MYSQL_YYABORT_ERROR(
                  ER_EXPLAIN_INTO_IMPLICIT_FORMAT_NOT_SUPPORTED, MYF(0));
              }
              if ($$.explain_format_type != Explain_format_type::JSON) {
                if ($$.explain_format_type == Explain_format_type::TREE) {
                  MYSQL_YYABORT_ERROR(ER_EXPLAIN_INTO_FORMAT_NOT_SUPPORTED,
                                      MYF(0), "TREE");
                } else {
                  MYSQL_YYABORT_ERROR(ER_EXPLAIN_INTO_FORMAT_NOT_SUPPORTED,
                                      MYF(0), "TRADITIONAL");
                }
              }
            }
            $$.explain_into_variable_name = $2;
          }
        ;

opt_explain_into:
          %empty
          {
            $$ = NULL_STR;
          }
        | INTO '@' ident_or_text
          {
            $$ = $3;
          }
        ;

opt_explain_for_schema:
          %empty
          {
            $$ = NULL_CSTR;
          }
        | FOR_SYM DATABASE ident_or_text
          {
            $$ = to_lex_cstring($3);
          }
        ;

opt_describe_column:
          %empty { $$= LEX_STRING{ nullptr, 0 }; }
        | text_string
          {
            if ($1 != nullptr)
              $$= $1->lex_string();
          }
        | ident
        ;


/* flush things */

flush:
          FLUSH_SYM opt_no_write_to_binlog
          {
            LEX *lex=Lex;
            lex->sql_command= SQLCOM_FLUSH;
            lex->type= 0;
            lex->no_write_to_binlog= $2;
          }
          flush_options
          {}
        ;

flush_options:
          table_or_tables opt_table_list
          {
            Lex->type|= REFRESH_TABLES;
            /*
              Set type of metadata and table locks for
              FLUSH TABLES table_list [WITH READ LOCK].
            */
            YYPS->m_lock_type= TL_READ_NO_INSERT;
            YYPS->m_mdl_type= MDL_SHARED_HIGH_PRIO;
            if (Select->add_tables(YYTHD, $2, TL_OPTION_UPDATING,
                                   YYPS->m_lock_type, YYPS->m_mdl_type))
              MYSQL_YYABORT;
          }
          opt_flush_lock {}
        | flush_options_list
        ;

opt_flush_lock:
          %empty {}
        | WITH READ_SYM LOCK_SYM
          {
            Table_ref *tables= Lex->query_tables;
            Lex->type|= REFRESH_READ_LOCK;
            for (; tables; tables= tables->next_global)
            {
              tables->mdl_request.set_type(MDL_SHARED_NO_WRITE);
              /* Don't try to flush views. */
              tables->required_type= dd::enum_table_type::BASE_TABLE;
              tables->open_type= OT_BASE_ONLY;      /* Ignore temporary tables. */
            }
          }
        | FOR_SYM
          {
            if (Lex->query_tables == nullptr) // Table list can't be empty
            {
              YYTHD->syntax_error(ER_NO_TABLES_USED);
              MYSQL_YYABORT;
            }
          }
          EXPORT_SYM
          {
            Table_ref *tables= Lex->query_tables;
            Lex->type|= REFRESH_FOR_EXPORT;
            for (; tables; tables= tables->next_global)
            {
              tables->mdl_request.set_type(MDL_SHARED_NO_WRITE);
              /* Don't try to flush views. */
              tables->required_type= dd::enum_table_type::BASE_TABLE;
              tables->open_type= OT_BASE_ONLY;      /* Ignore temporary tables. */
            }
          }
        ;

flush_options_list:
          flush_options_list ',' flush_option
        | flush_option
          {}
        ;

flush_option:
          ERROR_SYM LOGS_SYM
          { Lex->type|= REFRESH_ERROR_LOG; }
        | ENGINE_SYM LOGS_SYM
          { Lex->type|= REFRESH_ENGINE_LOG; }
        | GENERAL LOGS_SYM
          { Lex->type|= REFRESH_GENERAL_LOG; }
        | SLOW LOGS_SYM
          { Lex->type|= REFRESH_SLOW_LOG; }
        | BINARY_SYM LOGS_SYM
          { Lex->type|= REFRESH_BINARY_LOG; }
        | RELAY LOGS_SYM opt_channel
          {
            Lex->type|= REFRESH_RELAY_LOG;
            if (Lex->set_channel_name($3))
              MYSQL_YYABORT;  // OOM
          }
        | PRIVILEGES
          { Lex->type|= REFRESH_GRANT; }
        | LOGS_SYM
          { Lex->type|= REFRESH_LOG; }
        | STATUS_SYM
          { Lex->type|= REFRESH_STATUS; }
        | RESOURCES
          { Lex->type|= REFRESH_USER_RESOURCES; }
        | OPTIMIZER_COSTS_SYM
          { Lex->type|= REFRESH_OPTIMIZER_COSTS; }
        ;

opt_table_list:
          %empty { $$= nullptr; }
        | table_list
        ;

reset:
          RESET_SYM
          {
            LEX *lex=Lex;
            lex->sql_command= SQLCOM_RESET; lex->type=0;
          }
          reset_options
          {}
        | RESET_SYM PERSIST_SYM opt_if_exists_ident
          {
            LEX *lex=Lex;
            lex->sql_command= SQLCOM_RESET;
            lex->type|= REFRESH_PERSIST;
            lex->option_type= OPT_PERSIST;
          }
        ;

reset_options:
          reset_options ',' reset_option
        | reset_option
        ;

opt_if_exists_ident:
          %empty
          {
            LEX *lex=Lex;
            lex->drop_if_exists= false;
            lex->name= NULL_STR;
          }
        | if_exists persisted_variable_ident
          {
            LEX *lex=Lex;
            lex->drop_if_exists= $1;
            lex->name= $2;
          }
        ;

persisted_variable_ident:
          ident
        | ident '.' ident
          {
            const LEX_STRING prefix = $1;
            const LEX_STRING suffix = $3;
            $$.length = prefix.length + 1 + suffix.length + 1;
            $$.str = static_cast<char *>(YYTHD->alloc($$.length));
            if ($$.str == nullptr) YYABORT;  // OOM
            strxnmov($$.str, $$.length, prefix.str, ".", suffix.str, nullptr);
          }
        | DEFAULT_SYM '.' ident
          {
            const LEX_CSTRING prefix{STRING_WITH_LEN("default")};
            const LEX_STRING suffix = $3;
            $$.length = prefix.length + 1 + suffix.length + 1;
            $$.str = static_cast<char *>(YYTHD->alloc($$.length));
            if ($$.str == nullptr) YYABORT;  // OOM
            strxnmov($$.str, $$.length, prefix.str, ".", suffix.str, nullptr);
          }
        ;

reset_option:
          SLAVE
            {
              Lex->type|= REFRESH_SLAVE;
              Lex->set_replication_deprecated_syntax_used();
              push_deprecated_warn(YYTHD, "RESET SLAVE", "RESET REPLICA");
            }
          opt_replica_reset_options opt_channel
          {
            if (Lex->set_channel_name($4))
              MYSQL_YYABORT;  // OOM
          }
        | REPLICA_SYM
          { Lex->type|= REFRESH_REPLICA; }
          opt_replica_reset_options opt_channel
          {
          if (Lex->set_channel_name($4))
            MYSQL_YYABORT;  // OOM
          }
        | master_or_binary_logs_and_gtids
          {
            Lex->type|= REFRESH_SOURCE;
            if (Lex->is_replication_deprecated_syntax_used()){
              Lex->type|= REFRESH_MASTER;
              push_deprecated_warn(YYTHD, "RESET MASTER", "RESET BINARY LOGS AND GTIDS");
            }
            /*
              RESET BINARY LOGS AND GTIDS should acquire global read lock
              in order to avoid any parallel transaction commits
              while the reset operation is going on.

              *Only if* the thread is not already acquired the global
              read lock, server will acquire global read lock
              during the operation and release it at the
              end of the reset operation.
            */
            if (!(YYTHD)->global_read_lock.is_acquired())
              Lex->type|= REFRESH_TABLES | REFRESH_READ_LOCK;
          }
          source_reset_options
        ;

opt_replica_reset_options:
          %empty      { Lex->reset_slave_info.all= false; }
        | ALL         { Lex->reset_slave_info.all= true; }
        ;

source_reset_options:
          %empty {}
        | TO_SYM real_ulonglong_num
          {
            if ($2 == 0 || $2 > MAX_ALLOWED_FN_EXT_RESET_MASTER)
            {
              my_error(ER_RESET_SOURCE_TO_VALUE_OUT_OF_RANGE, MYF(0),
                       $2, MAX_ALLOWED_FN_EXT_RESET_MASTER);
              MYSQL_YYABORT;
            }
            else
              Lex->next_binlog_file_nr = $2;
          }
        ;

purge:
          PURGE
          {
            LEX *lex=Lex;
            lex->type=0;
            lex->sql_command = SQLCOM_PURGE;
          }
          purge_options
          {}
        ;

purge_options:
          master_or_binary
          {
            if (Lex->is_replication_deprecated_syntax_used())
            {
              push_deprecated_warn(YYTHD, "PURGE MASTER LOGS TO", "PURGE BINARY LOGS TO");
            }
          }
          LOGS_SYM purge_option
        ;

purge_option:
          TO_SYM TEXT_STRING_sys
          {
            Lex->to_log = $2.str;
          }
        | BEFORE_SYM expr
          {
            ITEMIZE($2, &$2);

            LEX *lex= Lex;
            lex->purge_value_list.clear();
            lex->purge_value_list.push_front($2);
            lex->sql_command= SQLCOM_PURGE_BEFORE;
          }
        ;

/* kill threads */

kill:
          KILL_SYM kill_option expr
          {
            ITEMIZE($3, &$3);

            LEX *lex=Lex;
            lex->kill_value_list.clear();
            lex->kill_value_list.push_front($3);
            lex->sql_command= SQLCOM_KILL;
          }
        ;

kill_option:
          %empty         { Lex->type= 0; }
        | CONNECTION_SYM { Lex->type= 0; }
        | QUERY_SYM      { Lex->type= ONLY_KILL_QUERY; }
        ;

/* change database */

use:
          USE_SYM ident
          {
            LEX *lex=Lex;
            lex->sql_command=SQLCOM_CHANGE_DB;
            lex->query_block->db= $2.str;
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

opt_duplicate:
          %empty { $$= On_duplicate::ERROR; }
        | duplicate
        ;

duplicate:
          REPLACE_SYM { $$= On_duplicate::REPLACE_DUP; }
        | IGNORE_SYM  { $$= On_duplicate::IGNORE_DUP; }
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

role_ident_or_text:
          role_ident
        | TEXT_STRING_sys
        | LEX_HOSTNAME
        ;

user_ident_or_text:
          ident_or_text
          {
            if (!($$= LEX_USER::alloc(YYTHD, &$1, nullptr)))
              MYSQL_YYABORT;
          }
        | ident_or_text '@' ident_or_text
          {
            if (!($$= LEX_USER::alloc(YYTHD, &$1, &$3)))
              MYSQL_YYABORT;
          }
        ;

user:
          user_ident_or_text
          {
            $$=$1;
          }
        | CURRENT_USER optional_braces
          {
            if (!($$= LEX_USER::alloc(YYTHD)))
              MYSQL_YYABORT;
            /*
              empty LEX_USER means current_user and
              will be handled in the  get_current_user() function
              later
            */
          }
        ;

role:
          role_ident_or_text
          {
            if (!($$= LEX_USER::alloc(YYTHD, &$1, nullptr)))
              MYSQL_YYABORT;
          }
        | role_ident_or_text '@' ident_or_text
          {
            if (!($$= LEX_USER::alloc(YYTHD, &$1, &$3)))
              MYSQL_YYABORT;
          }
        ;

schema:
          ident
          {
            $$ = $1;
            if (check_and_convert_db_name(&$$, false) != Ident_name_check::OK)
              MYSQL_YYABORT;
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

opt_var_type:
          %empty      { $$=OPT_SESSION; }
        | GLOBAL_SYM  { $$=OPT_GLOBAL; }
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

lvalue_variable:
          lvalue_ident
          {
            $$ = Bipartite_name{{}, to_lex_cstring($1)};
          }
        | lvalue_ident '.' ident
          {
            /*
              Reject names prefixed by `GLOBAL.`, `LOCAL.`, or `SESSION.` --
              if one of those prefixes is there then we are parsing something
              like `GLOBAL.GLOBAL.foo` or `LOCAL.SESSION.bar` etc.
            */
            if (check_reserved_words($1.str)) {
              YYTHD->syntax_error_at(@1);
              MYSQL_YYABORT;
            }
            $$ = Bipartite_name{to_lex_cstring($1), to_lex_cstring($3)};
          }
        | DEFAULT_SYM '.' ident
          {
            $$ = Bipartite_name{{STRING_WITH_LEN("default")}, to_lex_cstring($3)};
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

/* Lock function */

lock:
          LOCK_SYM table_or_tables
          {
            LEX *lex= Lex;

            if (lex->sphead)
            {
              my_error(ER_SP_BADSTATEMENT, MYF(0), "LOCK");
              MYSQL_YYABORT;
            }
            lex->sql_command= SQLCOM_LOCK_TABLES;
          }
          table_lock_list
          {}
        | LOCK_SYM INSTANCE_SYM FOR_SYM BACKUP_SYM
          {
            Lex->sql_command= SQLCOM_LOCK_INSTANCE;
            Lex->m_sql_cmd= NEW_PTN Sql_cmd_lock_instance();
            if (Lex->m_sql_cmd == nullptr)
              MYSQL_YYABORT; // OOM
          }
        ;

table_or_tables:
          TABLE_SYM
        | TABLES
        ;

table_lock_list:
          table_lock
        | table_lock_list ',' table_lock
        ;

table_lock:
          table_ident opt_table_alias lock_option
          {
            thr_lock_type lock_type= (thr_lock_type) $3;
            enum_mdl_type mdl_lock_type;

            if (lock_type >= TL_WRITE_ALLOW_WRITE)
            {
              /* LOCK TABLE ... WRITE/LOW_PRIORITY WRITE */
              mdl_lock_type= MDL_SHARED_NO_READ_WRITE;
            }
            else if (lock_type == TL_READ)
            {
              /* LOCK TABLE ... READ LOCAL */
              mdl_lock_type= MDL_SHARED_READ;
            }
            else
            {
              /* LOCK TABLE ... READ */
              mdl_lock_type= MDL_SHARED_READ_ONLY;
            }

            if (!Select->add_table_to_list(YYTHD, $1, $2.str, 0, lock_type,
                                           mdl_lock_type))
              MYSQL_YYABORT;
          }
        ;

lock_option:
          READ_SYM               { $$= TL_READ_NO_INSERT; }
        | WRITE_SYM              { $$= TL_WRITE_DEFAULT; }
        | LOW_PRIORITY WRITE_SYM
          {
            $$= TL_WRITE_LOW_PRIORITY;
            push_deprecated_warn(YYTHD, "LOW_PRIORITY WRITE", "WRITE");
          }
        | READ_SYM LOCAL_SYM     { $$= TL_READ; }
        ;

unlock:
          UNLOCK_SYM
          {
            LEX *lex= Lex;

            if (lex->sphead)
            {
              my_error(ER_SP_BADSTATEMENT, MYF(0), "UNLOCK");
              MYSQL_YYABORT;
            }
            lex->sql_command= SQLCOM_UNLOCK_TABLES;
          }
          table_or_tables
          {}
        | UNLOCK_SYM INSTANCE_SYM
          {
            Lex->sql_command= SQLCOM_UNLOCK_INSTANCE;
            Lex->m_sql_cmd= NEW_PTN Sql_cmd_unlock_instance();
            if (Lex->m_sql_cmd == nullptr)
              MYSQL_YYABORT; // OOM
          }
        ;


shutdown_stmt:
          SHUTDOWN
          {
            Lex->sql_command= SQLCOM_SHUTDOWN;
            $$= NEW_PTN PT_shutdown();
          }
        ;

restart_server_stmt:
          RESTART_SYM
          {
            $$= NEW_PTN PT_restart_server();
          }
        ;

alter_instance_stmt:
          ALTER INSTANCE_SYM alter_instance_action
          {
            Lex->sql_command= SQLCOM_ALTER_INSTANCE;
            $$= $3;
          }

alter_instance_action:
          ROTATE_SYM ident_or_text MASTER_SYM KEY_SYM
          {
            if (is_identifier($2, "INNODB"))
            {
              $$= NEW_PTN PT_alter_instance(@$, ROTATE_INNODB_MASTER_KEY, EMPTY_CSTR);
            }
            else if (is_identifier($2, "BINLOG"))
            {
              $$= NEW_PTN PT_alter_instance(@$, ROTATE_BINLOG_MASTER_KEY, EMPTY_CSTR);
            }
            else
            {
              YYTHD->syntax_error_at(@2);
              MYSQL_YYABORT;
            }
          }
        | RELOAD TLS_SYM
          {
            $$ = NEW_PTN PT_alter_instance(@$, ALTER_INSTANCE_RELOAD_TLS_ROLLBACK_ON_ERROR, to_lex_cstring("mysql_main"));
          }
        | RELOAD TLS_SYM NO_SYM ROLLBACK_SYM ON_SYM ERROR_SYM
          {
            $$ = NEW_PTN PT_alter_instance(@$, ALTER_INSTANCE_RELOAD_TLS, to_lex_cstring("mysql_main"));
          }
        | RELOAD TLS_SYM FOR_SYM CHANNEL_SYM ident {
            $$ = NEW_PTN PT_alter_instance(@$, ALTER_INSTANCE_RELOAD_TLS_ROLLBACK_ON_ERROR, to_lex_cstring($5));
          }
        | RELOAD TLS_SYM FOR_SYM CHANNEL_SYM ident NO_SYM ROLLBACK_SYM ON_SYM ERROR_SYM {
            $$ = NEW_PTN PT_alter_instance(@$, ALTER_INSTANCE_RELOAD_TLS, to_lex_cstring($5));
          }
        | ENABLE_SYM ident ident
          {
            if (!is_identifier($2, "INNODB"))
            {
              YYTHD->syntax_error_at(@2);
              MYSQL_YYABORT;
            }

            if (!is_identifier($3, "REDO_LOG"))
            {
              YYTHD->syntax_error_at(@3);
              MYSQL_YYABORT;
            }
            $$ = NEW_PTN PT_alter_instance(@$, ALTER_INSTANCE_ENABLE_INNODB_REDO, EMPTY_CSTR);
          }
        | DISABLE_SYM ident ident
          {
            if (!is_identifier($2, "INNODB"))
            {
              YYTHD->syntax_error_at(@2);
              MYSQL_YYABORT;
            }

            if (!is_identifier($3, "REDO_LOG"))
            {
              YYTHD->syntax_error_at(@3);
              MYSQL_YYABORT;
            }
            $$ = NEW_PTN PT_alter_instance(@$, ALTER_INSTANCE_DISABLE_INNODB_REDO, EMPTY_CSTR);
          }
        | RELOAD KEYRING_SYM {
            $$ = NEW_PTN PT_alter_instance(@$, RELOAD_KEYRING, EMPTY_CSTR);
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

/* GRANT / REVOKE */

revoke:
          REVOKE if_exists role_or_privilege_list FROM user_list opt_ignore_unknown_user
          {
            Lex->grant_if_exists = $2;
            Lex->ignore_unknown_user = $6;
            auto *tmp= NEW_PTN PT_revoke_roles(@$, $3, $5);
            MAKE_CMD(tmp);
          }
        | REVOKE if_exists role_or_privilege_list ON_SYM opt_acl_type grant_ident FROM user_list opt_ignore_unknown_user
          {
            LEX *lex= Lex;
            lex->grant_if_exists = $2;
            Lex->ignore_unknown_user = $9;
            if (apply_privileges(YYTHD, *$3))
              MYSQL_YYABORT;
            lex->sql_command= (lex->grant == GLOBAL_ACLS) ? SQLCOM_REVOKE_ALL
                                                          : SQLCOM_REVOKE;
            if ($5 != Acl_type::TABLE && !lex->columns.is_empty())
            {
              YYTHD->syntax_error();
              MYSQL_YYABORT;
            }
            lex->type= static_cast<ulong>($5);
            lex->users_list= *$8;
            MAKE_CMD_DCL_DUMMY();
          }
        | REVOKE if_exists ALL opt_privileges
          {
            Lex->grant_if_exists = $2;
            Lex->all_privileges= 1;
            Lex->grant= GLOBAL_ACLS;
          }
          ON_SYM opt_acl_type grant_ident FROM user_list opt_ignore_unknown_user
          {
            LEX *lex= Lex;
            lex->sql_command= (lex->grant == (GLOBAL_ACLS & ~GRANT_ACL)) ?
                                                            SQLCOM_REVOKE_ALL
                                                          : SQLCOM_REVOKE;
            if ($7 != Acl_type::TABLE && !lex->columns.is_empty())
            {
              YYTHD->syntax_error();
              MYSQL_YYABORT;
            }
            lex->type= static_cast<ulong>($7);
            lex->users_list= *$10;
            lex->ignore_unknown_user = $11;
            MAKE_CMD_DCL_DUMMY();
          }
        | REVOKE if_exists ALL opt_privileges ',' GRANT OPTION FROM user_list opt_ignore_unknown_user
          {
            Lex->grant_if_exists = $2;
            Lex->ignore_unknown_user = $10;
            Lex->sql_command = SQLCOM_REVOKE_ALL;
            Lex->users_list= *$9;
            MAKE_CMD_DCL_DUMMY();
          }
        | REVOKE if_exists PROXY_SYM ON_SYM user FROM user_list opt_ignore_unknown_user
          {
            LEX *lex= Lex;
            lex->grant_if_exists = $2;
            lex->ignore_unknown_user = $8;
            lex->sql_command= SQLCOM_REVOKE;
            lex->users_list= *$7;
            lex->users_list.push_front ($5);
            lex->type= TYPE_ENUM_PROXY;
            MAKE_CMD_DCL_DUMMY();
          }
        ;

grant:
          GRANT role_or_privilege_list TO_SYM user_list opt_with_admin_option
          {
            auto *tmp= NEW_PTN PT_grant_roles(@$, $2, $4, $5);
            MAKE_CMD(tmp);
          }
        | GRANT role_or_privilege_list ON_SYM opt_acl_type grant_ident TO_SYM user_list
          grant_options opt_grant_as
          {
            LEX *lex= Lex;
            lex->sql_command= SQLCOM_GRANT;
            if (apply_privileges(YYTHD, *$2))
              MYSQL_YYABORT;

            if ($4 != Acl_type::TABLE && !lex->columns.is_empty())
            {
              YYTHD->syntax_error();
              MYSQL_YYABORT;
            }
            lex->type= static_cast<ulong>($4);
            lex->users_list= *$7;
            MAKE_CMD_DCL_DUMMY();
          }
        | GRANT ALL opt_privileges
          {
            Lex->all_privileges= 1;
            Lex->grant= GLOBAL_ACLS;
          }
          ON_SYM opt_acl_type grant_ident TO_SYM user_list grant_options opt_grant_as
          {
            LEX *lex= Lex;
            lex->sql_command= SQLCOM_GRANT;
            if ($6 != Acl_type::TABLE && !lex->columns.is_empty())
            {
              YYTHD->syntax_error();
              MYSQL_YYABORT;
            }
            lex->type= static_cast<ulong>($6);
            lex->users_list= *$9;
            MAKE_CMD_DCL_DUMMY();
          }
        | GRANT PROXY_SYM ON_SYM user TO_SYM user_list opt_grant_option
          {
            LEX *lex= Lex;
            lex->sql_command= SQLCOM_GRANT;
            if ($7)
              lex->grant |= GRANT_ACL;
            lex->users_list= *$6;
            lex->users_list.push_front ($4);
            lex->type= TYPE_ENUM_PROXY;
            MAKE_CMD_DCL_DUMMY();
          }
        ;

opt_acl_type:
          %empty        { $$= Acl_type::TABLE; }
        | TABLE_SYM     { $$= Acl_type::TABLE; }
        | FUNCTION_SYM  { $$= Acl_type::FUNCTION; }
        | PROCEDURE_SYM { $$= Acl_type::PROCEDURE; }
        ;

opt_privileges:
          %empty
        | PRIVILEGES
        ;

role_or_privilege_list:
          role_or_privilege
          {
            $$= NEW_PTN Mem_root_array<PT_role_or_privilege *>(YYMEM_ROOT);
            if ($$ == nullptr || $$->push_back($1))
              MYSQL_YYABORT; // OOM
          }
        | role_or_privilege_list ',' role_or_privilege
          {
            $$= $1;
            if ($$->push_back($3))
              MYSQL_YYABORT; // OOM
          }
        ;

role_or_privilege:
          role_ident_or_text opt_column_list
          {
            if ($2 == nullptr)
              $$= NEW_PTN PT_role_or_dynamic_privilege(@$, @1, $1);
            else
              $$= NEW_PTN PT_dynamic_privilege(@$, @1, $1);
          }
        | role_ident_or_text '@' ident_or_text
          { $$= NEW_PTN PT_role_at_host(@$, @1, $1, $3); }
        | SELECT_SYM opt_column_list
          { $$= NEW_PTN PT_static_privilege(@$, @1, SELECT_ACL, $2); }
        | INSERT_SYM opt_column_list
          { $$= NEW_PTN PT_static_privilege(@$, @1, INSERT_ACL, $2); }
        | UPDATE_SYM opt_column_list
          { $$= NEW_PTN PT_static_privilege(@$, @1, UPDATE_ACL, $2); }
        | REFERENCES opt_column_list
          { $$= NEW_PTN PT_static_privilege(@$, @1, REFERENCES_ACL, $2); }
        | DELETE_SYM
          { $$= NEW_PTN PT_static_privilege(@$, @1, DELETE_ACL); }
        | USAGE
          { $$= NEW_PTN PT_static_privilege(@$, @1, 0); }
        | INDEX_SYM
          { $$= NEW_PTN PT_static_privilege(@$, @1, INDEX_ACL); }
        | ALTER
          { $$= NEW_PTN PT_static_privilege(@$, @1, ALTER_ACL); }
        | CREATE
          { $$= NEW_PTN PT_static_privilege(@$, @1, CREATE_ACL); }
        | DROP
          { $$= NEW_PTN PT_static_privilege(@$, @1, DROP_ACL); }
        | EXECUTE_SYM
          { $$= NEW_PTN PT_static_privilege(@$, @1, EXECUTE_ACL); }
        | RELOAD
          { $$= NEW_PTN PT_static_privilege(@$, @1, RELOAD_ACL); }
        | SHUTDOWN
          { $$= NEW_PTN PT_static_privilege(@$, @1, SHUTDOWN_ACL); }
        | PROCESS
          { $$= NEW_PTN PT_static_privilege(@$, @1, PROCESS_ACL); }
        | FILE_SYM
          { $$= NEW_PTN PT_static_privilege(@$, @1, FILE_ACL); }
        | GRANT OPTION
          {
            $$= NEW_PTN PT_static_privilege(@$, @1, GRANT_ACL);
            Lex->grant_privilege= true;
          }
        | SHOW DATABASES
          { $$= NEW_PTN PT_static_privilege(@$, @1, SHOW_DB_ACL); }
        | SUPER_SYM
          {
            /* DEPRECATED */
            $$= NEW_PTN PT_static_privilege(@$, @1, SUPER_ACL);
            if (Lex->grant != GLOBAL_ACLS)
            {
              /*
                 An explicit request was made for the SUPER priv id
              */
              push_warning(Lex->thd, Sql_condition::SL_WARNING,
                           ER_WARN_DEPRECATED_SYNTAX,
                           "The SUPER privilege identifier is deprecated");
            }
          }
        | CREATE TEMPORARY TABLES
          { $$= NEW_PTN PT_static_privilege(@$, @1, CREATE_TMP_ACL); }
        | LOCK_SYM TABLES
          { $$= NEW_PTN PT_static_privilege(@$, @1, LOCK_TABLES_ACL); }
        | REPLICATION SLAVE
          { $$= NEW_PTN PT_static_privilege(@$, @1, REPL_SLAVE_ACL); }
        | REPLICATION CLIENT_SYM
          { $$= NEW_PTN PT_static_privilege(@$, @1, REPL_CLIENT_ACL); }
        | CREATE VIEW_SYM
          { $$= NEW_PTN PT_static_privilege(@$, @1, CREATE_VIEW_ACL); }
        | SHOW VIEW_SYM
          { $$= NEW_PTN PT_static_privilege(@$, @1, SHOW_VIEW_ACL); }
        | CREATE ROUTINE_SYM
          { $$= NEW_PTN PT_static_privilege(@$, @1, CREATE_PROC_ACL); }
        | ALTER ROUTINE_SYM
          { $$= NEW_PTN PT_static_privilege(@$, @1, ALTER_PROC_ACL); }
        | CREATE USER
          { $$= NEW_PTN PT_static_privilege(@$, @1, CREATE_USER_ACL); }
        | EVENT_SYM
          { $$= NEW_PTN PT_static_privilege(@$, @1, EVENT_ACL); }
        | TRIGGER_SYM
          { $$= NEW_PTN PT_static_privilege(@$, @1, TRIGGER_ACL); }
        | CREATE TABLESPACE_SYM
          { $$= NEW_PTN PT_static_privilege(@$, @1, CREATE_TABLESPACE_ACL); }
        | CREATE ROLE_SYM
          { $$= NEW_PTN PT_static_privilege(@$, @1, CREATE_ROLE_ACL); }
        | DROP ROLE_SYM
          { $$= NEW_PTN PT_static_privilege(@$, @1, DROP_ROLE_ACL); }
        ;

opt_with_admin_option:
          %empty                { $$= false; }
        | WITH ADMIN_SYM OPTION { $$= true; }
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

grant_ident:
          '*'
          {
            LEX *lex= Lex;
            size_t dummy;
            if (lex->copy_db_to(&lex->current_query_block()->db, &dummy))
              MYSQL_YYABORT;
            if (lex->grant == GLOBAL_ACLS)
              lex->grant = DB_OP_ACLS;
            else if (lex->columns.elements)
            {
              my_error(ER_ILLEGAL_GRANT_FOR_TABLE, MYF(0));
              MYSQL_YYABORT;
            }
          }
        | schema '.' '*'
          {
            LEX *lex= Lex;
            lex->current_query_block()->db = $1.str;
            if (lex->grant == GLOBAL_ACLS)
              lex->grant = DB_OP_ACLS;
            else if (lex->columns.elements)
            {
              my_error(ER_ILLEGAL_GRANT_FOR_TABLE, MYF(0));
              MYSQL_YYABORT;
            }
          }
        | '*' '.' '*'
          {
            LEX *lex= Lex;
            lex->current_query_block()->db = nullptr;
            if (lex->grant == GLOBAL_ACLS)
              lex->grant= GLOBAL_ACLS & ~GRANT_ACL;
            else if (lex->columns.elements)
            {
              my_error(ER_ILLEGAL_GRANT_FOR_TABLE, MYF(0));
              MYSQL_YYABORT;
            }
          }
        | ident
          {
            auto tmp = NEW_PTN Table_ident(to_lex_cstring($1));
            if (tmp == nullptr)
              MYSQL_YYABORT;
            LEX *lex=Lex;
            if (!lex->current_query_block()->add_table_to_list(lex->thd, tmp, nullptr,
                                                        TL_OPTION_UPDATING))
              MYSQL_YYABORT;
            if (lex->grant == GLOBAL_ACLS)
              lex->grant =  TABLE_OP_ACLS;
          }
        | schema '.' ident
          {
            auto schema_name = YYCLIENT_NO_SCHEMA ? LEX_CSTRING{}
                                                  : to_lex_cstring($1.str);
            auto tmp = NEW_PTN Table_ident(schema_name, to_lex_cstring($3));
            if (tmp == nullptr)
              MYSQL_YYABORT;
            LEX *lex=Lex;
            if (!lex->current_query_block()->add_table_to_list(lex->thd, tmp, nullptr,
                                                        TL_OPTION_UPDATING))
              MYSQL_YYABORT;
            if (lex->grant == GLOBAL_ACLS)
              lex->grant =  TABLE_OP_ACLS;
          }
        ;

user_list:
          user
          {
            $$= new (YYMEM_ROOT) List<LEX_USER>;
            if ($$ == nullptr || $$->push_back($1))
              MYSQL_YYABORT;
          }
        | user_list ',' user
          {
            $$= $1;
            if ($$->push_back($3))
              MYSQL_YYABORT;
          }
        ;

role_list:
          role
          {
            $$= new (YYMEM_ROOT) List<LEX_USER>;
            if ($$ == nullptr || $$->push_back($1))
              MYSQL_YYABORT;
          }
        | role_list ',' role
          {
            $$= $1;
            if ($$->push_back($3))
              MYSQL_YYABORT;
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

opt_column_list:
          %empty { $$= nullptr; }
        | '(' column_list ')' { $$= $2; }
        ;

column_list:
          ident
          {
            $$= NEW_PTN Mem_root_array<LEX_CSTRING>(YYMEM_ROOT);
            if ($$ == nullptr || $$->push_back(to_lex_cstring($1)))
              MYSQL_YYABORT; // OOM
          }
        | column_list ',' ident
          {
            $$= $1;
            if ($$->push_back(to_lex_cstring($3)))
              MYSQL_YYABORT; // OOM
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

grant_options:
          %empty {}
        | WITH GRANT OPTION
          { Lex->grant |= GRANT_ACL;}
        ;

opt_grant_option:
          %empty { $$= false; }
        | WITH GRANT OPTION { $$= true; }
        ;
opt_with_roles:
          %empty { Lex->grant_as.role_type = role_enum::ROLE_NONE; }
        | WITH ROLE_SYM role_list
          { Lex->grant_as.role_type = role_enum::ROLE_NAME;
            Lex->grant_as.role_list = $3;
          }
        | WITH ROLE_SYM ALL opt_except_role_list
          {
            Lex->grant_as.role_type = role_enum::ROLE_ALL;
            Lex->grant_as.role_list = $4;
          }
        | WITH ROLE_SYM NONE_SYM
          { Lex->grant_as.role_type = role_enum::ROLE_NONE; }
        | WITH ROLE_SYM DEFAULT_SYM
          { Lex->grant_as.role_type = role_enum::ROLE_DEFAULT; }

opt_grant_as:
          %empty { Lex->grant_as.grant_as_used = false; }
        | AS user opt_with_roles
          {
            Lex->grant_as.grant_as_used = true;
            Lex->grant_as.user = $2;
          }

begin_stmt:
          BEGIN_SYM
          {
            LEX *lex=Lex;
            lex->sql_command = SQLCOM_BEGIN;
            lex->start_transaction_opt= 0;
          }
          opt_work {}
        ;

opt_work:
          %empty {}
        | WORK_SYM  {}
        ;

opt_chain:
          %empty                   { $$= TVL_UNKNOWN; }
        | AND_SYM NO_SYM CHAIN_SYM { $$= TVL_NO; }
        | AND_SYM CHAIN_SYM        { $$= TVL_YES; }
        ;

opt_release:
          %empty             { $$= TVL_UNKNOWN; }
        | RELEASE_SYM        { $$= TVL_YES; }
        | NO_SYM RELEASE_SYM { $$= TVL_NO; }
;

opt_savepoint:
          %empty {}
        | SAVEPOINT_SYM {}
        ;

commit:
          COMMIT_SYM opt_work opt_chain opt_release
          {
            LEX *lex=Lex;
            lex->sql_command= SQLCOM_COMMIT;
            /* Don't allow AND CHAIN RELEASE. */
            MYSQL_YYABORT_UNLESS($3 != TVL_YES || $4 != TVL_YES);
            lex->tx_chain= $3;
            lex->tx_release= $4;
          }
        ;

rollback:
          ROLLBACK_SYM opt_work opt_chain opt_release
          {
            LEX *lex=Lex;
            lex->sql_command= SQLCOM_ROLLBACK;
            /* Don't allow AND CHAIN RELEASE. */
            MYSQL_YYABORT_UNLESS($3 != TVL_YES || $4 != TVL_YES);
            lex->tx_chain= $3;
            lex->tx_release= $4;
          }
        | ROLLBACK_SYM opt_work
          TO_SYM opt_savepoint ident
          {
            LEX *lex=Lex;
            lex->sql_command= SQLCOM_ROLLBACK_TO_SAVEPOINT;
            lex->ident= $5;
          }
        ;

savepoint:
          SAVEPOINT_SYM ident
          {
            LEX *lex=Lex;
            lex->sql_command= SQLCOM_SAVEPOINT;
            lex->ident= $2;
          }
        ;

release:
          RELEASE_SYM SAVEPOINT_SYM ident
          {
            LEX *lex=Lex;
            lex->sql_command= SQLCOM_RELEASE_SAVEPOINT;
            lex->ident= $3;
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

 DEFINER clause support.

**************************************************************************/

definer_opt:
          no_definer
        | definer
        ;

no_definer:
          %empty
          {
            /*
              We have to distinguish missing DEFINER-clause from case when
              CURRENT_USER specified as definer explicitly in order to properly
              handle CREATE TRIGGER statements which come to replication thread
              from older master servers (i.e. to create non-suid trigger in this
              case).
            */
            YYTHD->lex->definer= nullptr;
          }
        ;

definer:
          DEFINER_SYM EQ user
          {
            YYTHD->lex->definer= get_current_user(YYTHD, $3);
          }
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

view_check_option:
          %empty                          { $$= VIEW_CHECK_NONE; }
        | WITH CHECK_SYM OPTION           { $$= VIEW_CHECK_CASCADED; }
        | WITH CASCADED CHECK_SYM OPTION  { $$= VIEW_CHECK_CASCADED; }
        | WITH LOCAL_SYM CHECK_SYM OPTION { $$= VIEW_CHECK_LOCAL; }
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

/*************************************************************************/

xa:
          XA_SYM begin_or_start xid opt_join_or_resume
          {
            Lex->sql_command = SQLCOM_XA_START;
            Lex->m_sql_cmd= NEW_PTN Sql_cmd_xa_start($3, $4);
          }
        | XA_SYM END xid opt_suspend
          {
            Lex->sql_command = SQLCOM_XA_END;
            Lex->m_sql_cmd= NEW_PTN Sql_cmd_xa_end($3, $4);
          }
        | XA_SYM PREPARE_SYM xid
          {
            Lex->sql_command = SQLCOM_XA_PREPARE;
            Lex->m_sql_cmd= NEW_PTN Sql_cmd_xa_prepare($3);
          }
        | XA_SYM COMMIT_SYM xid opt_one_phase
          {
            Lex->sql_command = SQLCOM_XA_COMMIT;
            Lex->m_sql_cmd= NEW_PTN Sql_cmd_xa_commit($3, $4);
          }
        | XA_SYM ROLLBACK_SYM xid
          {
            Lex->sql_command = SQLCOM_XA_ROLLBACK;
            Lex->m_sql_cmd= NEW_PTN Sql_cmd_xa_rollback($3);
          }
        | XA_SYM RECOVER_SYM opt_convert_xid
          {
            Lex->sql_command = SQLCOM_XA_RECOVER;
            Lex->m_sql_cmd= NEW_PTN Sql_cmd_xa_recover($3);
          }
        ;

opt_convert_xid:
           %empty              { $$= false; }
         | CONVERT_SYM XID_SYM { $$= true; }

xid:
          text_string
          {
            MYSQL_YYABORT_UNLESS($1->length() <= MAXGTRIDSIZE);
            XID *xid;
            if (!(xid= (XID *)YYTHD->alloc(sizeof(XID))))
              MYSQL_YYABORT;
            xid->set(1L, $1->ptr(), $1->length(), nullptr, 0);
            $$= xid;
          }
          | text_string ',' text_string
          {
            MYSQL_YYABORT_UNLESS($1->length() <= MAXGTRIDSIZE &&
                                 $3->length() <= MAXBQUALSIZE);
            XID *xid;
            if (!(xid= (XID *)YYTHD->alloc(sizeof(XID))))
              MYSQL_YYABORT;
            xid->set(1L, $1->ptr(), $1->length(), $3->ptr(), $3->length());
            $$= xid;
          }
          | text_string ',' text_string ',' ulong_num
          {
            // check for overwflow of xid format id
            bool format_id_overflow_detected= ($5 > LONG_MAX);

            MYSQL_YYABORT_UNLESS($1->length() <= MAXGTRIDSIZE &&
                                 $3->length() <= MAXBQUALSIZE
                                 && !format_id_overflow_detected);

            XID *xid;
            if (!(xid= (XID *)YYTHD->alloc(sizeof(XID))))
              MYSQL_YYABORT;
            xid->set($5, $1->ptr(), $1->length(), $3->ptr(), $3->length());
            $$= xid;
          }
        ;

begin_or_start:
          BEGIN_SYM {}
        | START_SYM {}
        ;

opt_join_or_resume:
          %empty        { $$= XA_NONE;        }
        | JOIN_SYM      { $$= XA_JOIN;        }
        | RESUME_SYM    { $$= XA_RESUME;      }
        ;

opt_one_phase:
          %empty            { $$= XA_NONE;        }
        | ONE_SYM PHASE_SYM { $$= XA_ONE_PHASE;   }
        ;

opt_suspend:
          %empty { $$= XA_NONE;        }
        | SUSPEND_SYM
          { $$= XA_SUSPEND;     }
        | SUSPEND_SYM FOR_SYM MIGRATE_SYM
          { $$= XA_FOR_MIGRATE; }
        ;

install_option_type:
          %empty      { $$=OPT_GLOBAL; }
        | GLOBAL_SYM  { $$=OPT_GLOBAL; }
        | PERSIST_SYM { $$=OPT_PERSIST; }
        ;

install_set_rvalue:
          expr
        | ON_SYM
          {
            $$= NEW_PTN Item_string(@$, "ON", 2, system_charset_info);
          }
        ;

install_set_value:
        install_option_type lvalue_variable equal install_set_rvalue
        {
          $$ = NEW_PTN PT_install_component_set_element {$1, $2, $4};
        }
        ;

install_set_value_list:
        install_set_value
          {
            $$ = NEW_PTN List<PT_install_component_set_element>;
            if (!$$)
              MYSQL_YYABORT; // OOM
            if ($$->push_back($1))
              MYSQL_YYABORT; // OOM
          }
        | install_set_value_list ',' install_set_value
          {
            $$ = $1;
            if ($$->push_back($3))
              MYSQL_YYABORT; // OOM
          }
        ;

opt_install_set_value_list:
          %empty
          {
            $$ = NEW_PTN List<PT_install_component_set_element>;
          }
        | SET_SYM install_set_value_list { $$ = $2; }
        ;

install_stmt:
          INSTALL_SYM PLUGIN_SYM ident SONAME_SYM TEXT_STRING_sys
          {
            LEX *lex= Lex;
            lex->sql_command= SQLCOM_INSTALL_PLUGIN;
            lex->m_sql_cmd= new (YYMEM_ROOT) Sql_cmd_install_plugin(to_lex_cstring($3), $5);
            $$ = nullptr;
          }
        | INSTALL_SYM COMPONENT_SYM TEXT_STRING_sys_list opt_install_set_value_list
          {
            $$ = NEW_PTN PT_install_component(@$, YYTHD, $3, $4);
          }
        ;

uninstall:
          UNINSTALL_SYM PLUGIN_SYM ident
          {
            LEX *lex= Lex;
            lex->sql_command= SQLCOM_UNINSTALL_PLUGIN;
            lex->m_sql_cmd= new (YYMEM_ROOT) Sql_cmd_uninstall_plugin(to_lex_cstring($3));
          }
       | UNINSTALL_SYM COMPONENT_SYM TEXT_STRING_sys_list
          {
            LEX *lex= Lex;
            lex->sql_command= SQLCOM_UNINSTALL_COMPONENT;
            lex->m_sql_cmd= new (YYMEM_ROOT) Sql_cmd_uninstall_component($3);
          }
        ;

TEXT_STRING_sys_list:
          TEXT_STRING_sys
          {
            $$.init(YYTHD->mem_root);
            if ($$.push_back($1))
              MYSQL_YYABORT; // OOM
          }
        | TEXT_STRING_sys_list ',' TEXT_STRING_sys
          {
            $$= $1;
            if ($$.push_back($3))
              MYSQL_YYABORT; // OOM
          }
        ;

import_stmt:
          IMPORT TABLE_SYM FROM TEXT_STRING_sys_list
          {
            LEX *lex= Lex;
            lex->m_sql_cmd=
              new (YYTHD->mem_root) Sql_cmd_import_table($4);
            if (lex->m_sql_cmd == nullptr)
              MYSQL_YYABORT;
            lex->sql_command= SQLCOM_IMPORT;
          }
        ;

/**************************************************************************

Clone local/remote replica statements.

**************************************************************************/
clone_stmt:
          CLONE_SYM LOCAL_SYM
          DATA_SYM DIRECTORY_SYM opt_equal TEXT_STRING_filesystem
          {
            Lex->sql_command= SQLCOM_CLONE;
            Lex->m_sql_cmd= NEW_PTN Sql_cmd_clone(to_lex_cstring($6));
            if (Lex->m_sql_cmd == nullptr)
              MYSQL_YYABORT;
          }

        | CLONE_SYM INSTANCE_SYM FROM user ':' ulong_num
          IDENTIFIED_SYM BY TEXT_STRING_sys
          opt_datadir_ssl
          {
            Lex->sql_command= SQLCOM_CLONE;
            /* Reject space characters around ':' */
            if (@6.raw.start - @4.raw.end != 1) {
              YYTHD->syntax_error_at(@5);
              MYSQL_YYABORT;
            }
            $4->first_factor_auth_info.auth = to_lex_cstring($9);
            $4->first_factor_auth_info.uses_identified_by_clause = true;
            Lex->contains_plaintext_password= true;

            Lex->m_sql_cmd= NEW_PTN Sql_cmd_clone($4, $6, to_lex_cstring($10));

            if (Lex->m_sql_cmd == nullptr)
              MYSQL_YYABORT;
          }
        ;

opt_datadir_ssl:
          opt_ssl
          {
            $$= null_lex_str;
          }
        | DATA_SYM DIRECTORY_SYM opt_equal TEXT_STRING_filesystem opt_ssl
          {
            $$= $4;
          }
        ;

opt_ssl:
          %empty
          {
            Lex->ssl_type= SSL_TYPE_NOT_SPECIFIED;
          }
        | REQUIRE_SYM SSL_SYM
          {
            Lex->ssl_type= SSL_TYPE_SPECIFIED;
          }
        | REQUIRE_SYM NO_SYM SSL_SYM
          {
            Lex->ssl_type= SSL_TYPE_NONE;
          }
        ;

resource_group_types:
          USER { $$= resourcegroups::Type::USER_RESOURCE_GROUP; }
        | SYSTEM_SYM { $$= resourcegroups::Type::SYSTEM_RESOURCE_GROUP; }
        ;

opt_resource_group_vcpu_list:
          %empty
          {
            /* Make an empty list. */
            $$= NEW_PTN Mem_root_array<resourcegroups::Range>(YYMEM_ROOT);
            if ($$ == nullptr)
              MYSQL_YYABORT;
          }
        | VCPU_SYM opt_equal vcpu_range_spec_list { $$= $3; }
        ;

vcpu_range_spec_list:
          vcpu_num_or_range
          {
            resourcegroups::Range r($1.start, $1.end);
            $$= NEW_PTN Mem_root_array<resourcegroups::Range>(YYMEM_ROOT);
            if ($$ == nullptr || $$->push_back(r))
              MYSQL_YYABORT;
          }
        | vcpu_range_spec_list opt_comma vcpu_num_or_range
          {
            resourcegroups::Range r($3.start, $3.end);
            $$= $1;
            if ($$ == nullptr || $$->push_back(r))
              MYSQL_YYABORT;
          }
        ;

vcpu_num_or_range:
          NUM
          {
            auto cpu_id= my_strtoull($1.str, nullptr, 10);
            $$.start= $$.end=
              static_cast<resourcegroups::platform::cpu_id_t>(cpu_id);
            assert($$.start == cpu_id); // truncation check
          }
        | NUM '-' NUM
          {
            auto start= my_strtoull($1.str, nullptr, 10);
            $$.start= static_cast<resourcegroups::platform::cpu_id_t>(start);
            assert($$.start == start); // truncation check

            auto end= my_strtoull($3.str, nullptr, 10);
            $$.end= static_cast<resourcegroups::platform::cpu_id_t>(end);
            assert($$.end == end); // truncation check
          }
        ;

signed_num:
          NUM     { $$= static_cast<int>(my_strtoll($1.str, nullptr, 10)); }
        | '-' NUM { $$= -static_cast<int>(my_strtoll($2.str, nullptr, 10)); }
        ;

opt_resource_group_priority:
          %empty { $$.is_default= true; }
        | THREAD_PRIORITY_SYM opt_equal signed_num
          {
            $$.is_default= false;
            $$.value= $3;
          }
        ;

opt_resource_group_enable_disable:
          %empty { $$.is_default= true; }
        | ENABLE_SYM
          {
            $$.is_default= false;
            $$.value= true;
          }
        | DISABLE_SYM
          {
            $$.is_default= false;
            $$.value= false;
          }
        ;

opt_force:
          %empty      { $$= false; }
        | FORCE_SYM   { $$= true; }
        ;
