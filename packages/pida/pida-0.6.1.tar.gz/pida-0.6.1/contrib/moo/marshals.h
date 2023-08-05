
#ifndef ___moo_marshal_MARSHAL_H__
#define ___moo_marshal_MARSHAL_H__

#include	<glib-object.h>

G_BEGIN_DECLS

/* BOOL:BOXED (marshals.list:1) */
extern void _moo_marshal_BOOLEAN__BOXED (GClosure     *closure,
                                         GValue       *return_value,
                                         guint         n_param_values,
                                         const GValue *param_values,
                                         gpointer      invocation_hint,
                                         gpointer      marshal_data);
#define _moo_marshal_BOOL__BOXED	_moo_marshal_BOOLEAN__BOXED

/* BOOL:INT (marshals.list:2) */
extern void _moo_marshal_BOOLEAN__INT (GClosure     *closure,
                                       GValue       *return_value,
                                       guint         n_param_values,
                                       const GValue *param_values,
                                       gpointer      invocation_hint,
                                       gpointer      marshal_data);
#define _moo_marshal_BOOL__INT	_moo_marshal_BOOLEAN__INT

/* BOOL:OBJECT,BOXED (marshals.list:3) */
extern void _moo_marshal_BOOLEAN__OBJECT_BOXED (GClosure     *closure,
                                                GValue       *return_value,
                                                guint         n_param_values,
                                                const GValue *param_values,
                                                gpointer      invocation_hint,
                                                gpointer      marshal_data);
#define _moo_marshal_BOOL__OBJECT_BOXED	_moo_marshal_BOOLEAN__OBJECT_BOXED

/* BOOL:OBJECT,BOXED,BOXED (marshals.list:4) */
extern void _moo_marshal_BOOLEAN__OBJECT_BOXED_BOXED (GClosure     *closure,
                                                      GValue       *return_value,
                                                      guint         n_param_values,
                                                      const GValue *param_values,
                                                      gpointer      invocation_hint,
                                                      gpointer      marshal_data);
#define _moo_marshal_BOOL__OBJECT_BOXED_BOXED	_moo_marshal_BOOLEAN__OBJECT_BOXED_BOXED

/* BOOL:OBJECT,OBJECT (marshals.list:5) */
extern void _moo_marshal_BOOLEAN__OBJECT_OBJECT (GClosure     *closure,
                                                 GValue       *return_value,
                                                 guint         n_param_values,
                                                 const GValue *param_values,
                                                 gpointer      invocation_hint,
                                                 gpointer      marshal_data);
#define _moo_marshal_BOOL__OBJECT_OBJECT	_moo_marshal_BOOLEAN__OBJECT_OBJECT

/* BOOL:STRING (marshals.list:6) */
extern void _moo_marshal_BOOLEAN__STRING (GClosure     *closure,
                                          GValue       *return_value,
                                          guint         n_param_values,
                                          const GValue *param_values,
                                          gpointer      invocation_hint,
                                          gpointer      marshal_data);
#define _moo_marshal_BOOL__STRING	_moo_marshal_BOOLEAN__STRING

/* BOOL:VOID (marshals.list:7) */
extern void _moo_marshal_BOOLEAN__VOID (GClosure     *closure,
                                        GValue       *return_value,
                                        guint         n_param_values,
                                        const GValue *param_values,
                                        gpointer      invocation_hint,
                                        gpointer      marshal_data);
#define _moo_marshal_BOOL__VOID	_moo_marshal_BOOLEAN__VOID

/* VOID:BOXED,POINTER (marshals.list:8) */
extern void _moo_marshal_VOID__BOXED_POINTER (GClosure     *closure,
                                              GValue       *return_value,
                                              guint         n_param_values,
                                              const GValue *param_values,
                                              gpointer      invocation_hint,
                                              gpointer      marshal_data);

/* VOID:INT (marshals.list:9) */
#define _moo_marshal_VOID__INT	g_cclosure_marshal_VOID__INT

/* VOID:OBJECT (marshals.list:10) */
#define _moo_marshal_VOID__OBJECT	g_cclosure_marshal_VOID__OBJECT

/* VOID:OBJECT,BOOL (marshals.list:11) */
extern void _moo_marshal_VOID__OBJECT_BOOLEAN (GClosure     *closure,
                                               GValue       *return_value,
                                               guint         n_param_values,
                                               const GValue *param_values,
                                               gpointer      invocation_hint,
                                               gpointer      marshal_data);
#define _moo_marshal_VOID__OBJECT_BOOL	_moo_marshal_VOID__OBJECT_BOOLEAN

/* VOID:OBJECT,BOXED,BOXED (marshals.list:12) */
extern void _moo_marshal_VOID__OBJECT_BOXED_BOXED (GClosure     *closure,
                                                   GValue       *return_value,
                                                   guint         n_param_values,
                                                   const GValue *param_values,
                                                   gpointer      invocation_hint,
                                                   gpointer      marshal_data);

/* VOID:POINTER (marshals.list:13) */
#define _moo_marshal_VOID__POINTER	g_cclosure_marshal_VOID__POINTER

/* VOID:POINTER,BOOLEAN (marshals.list:14) */
extern void _moo_marshal_VOID__POINTER_BOOLEAN (GClosure     *closure,
                                                GValue       *return_value,
                                                guint         n_param_values,
                                                const GValue *param_values,
                                                gpointer      invocation_hint,
                                                gpointer      marshal_data);

/* VOID:POINTER,POINTER (marshals.list:15) */
extern void _moo_marshal_VOID__POINTER_POINTER (GClosure     *closure,
                                                GValue       *return_value,
                                                guint         n_param_values,
                                                const GValue *param_values,
                                                gpointer      invocation_hint,
                                                gpointer      marshal_data);

/* VOID:STRING (marshals.list:16) */
#define _moo_marshal_VOID__STRING	g_cclosure_marshal_VOID__STRING

/* VOID:UINT (marshals.list:17) */
#define _moo_marshal_VOID__UINT	g_cclosure_marshal_VOID__UINT

/* VOID:VOID (marshals.list:18) */
#define _moo_marshal_VOID__VOID	g_cclosure_marshal_VOID__VOID

/* BOOL:VOID (marshals.list:19) */

/* VOID:INT (marshals.list:20) */

/* VOID:OBJECT (marshals.list:21) */

/* VOID:OBJECT,BOOL (marshals.list:22) */

/* VOID:UINT (marshals.list:23) */

G_END_DECLS

#endif /* ___moo_marshal_MARSHAL_H__ */

