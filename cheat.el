;;;; -*- lisp-interaction -*-

;;;; this is just a personal crutch to make it easier to develop using
;;;; aquamacs on a mac in combination with virtualenv.

(setenv "PATH" (concat (mapconcat
	 (function (lambda (x) x))
	 (reverse (cdr (reverse (split-string (buffer-file-name) "/")))) "/")
	"/elffile-dev/bin:"
	(getenv "PATH")))
