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

create:
          CREATE view_or_trigger_or_sp_or_event
          {}
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

// Start of option value list, option_type was given
start_option_value_list_following_option_type:
          option_value_following_option_type option_value_list_continued
          {
            $$=
              NEW_PTN PT_start_option_value_list_following_option_type_eq(@$, $1,
                                                                          @1,
                                                                          $2);
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
        ;

definer_tail:
          sp_tail
        | sf_tail
        | event_tail
        ;

no_definer_tail:
          sp_tail
        | sf_tail
        | udf_tail
        | event_tail
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
