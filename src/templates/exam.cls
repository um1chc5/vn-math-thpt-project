%% exam.cls — đề thi Toán THPT (XeLaTeX, tiếng Việt)
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{exam}[2026/09/17 De thi Toan THPT]

\LoadClass[12pt,a4paper]{article}

\RequirePackage{iftex}
\iftutex\else
  \ClassError{exam}{Can bien dich bang XeLaTeX (hoac LuaLaTeX)}{Dung: latexmk -xelatex hoac xelatex}
\fi

\RequirePackage[top=1.8cm,bottom=1.8cm,left=1.8cm,right=1.8cm]{geometry}
\RequirePackage{fontspec}
\RequirePackage{amsmath,amssymb,amsfonts}
\RequirePackage{xcolor}
\RequirePackage{enumitem}
\RequirePackage{array,tabularx}
\RequirePackage{setspace}

% Vietnamese text: Times New Roman on school machines, Liberation Serif on Linux.
\defaultfontfeatures{Ligatures=TeX,Scale=MatchLowercase}
\IfFontExistsTF{Times New Roman}{
  \setmainfont{Times New Roman}[Scale=1.0]
}{
  \IfFontExistsTF{Liberation Serif}{
    \setmainfont{Liberation Serif}[Scale=1.0]
  }{
    \setmainfont{DejaVu Serif}[Scale=1.0]
  }
}
\IfFontExistsTF{Arial}{
  \setsansfont{Arial}
}{
  \IfFontExistsTF{Liberation Sans}{
    \setsansfont{Liberation Sans}
  }{
    \setsansfont{DejaVu Sans}
  }
}
\IfFontExistsTF{Courier New}{
  \setmonofont{Courier New}[Scale=0.92]
}{
  \IfFontExistsTF{Liberation Mono}{
    \setmonofont{Liberation Mono}[Scale=0.92]
  }{
    \setmonofont{DejaVu Sans Mono}[Scale=0.92]
  }
}

\setstretch{1.15}
\setlength{\parindent}{0pt}
\setlength{\parskip}{0.35em}
\pagestyle{plain}
\setcounter{secnumdepth}{0}

% ----- metadata -----
\newcommand{\@school}{TRƯỜNG THPT}
\newcommand{\@department}{SỞ GIÁO DỤC VÀ ĐÀO TẠO}
\newcommand{\@examtitle}{ĐỀ KIỂM TRA}
\newcommand{\@subject}{Toán}
\newcommand{\@grade}{}
\newcommand{\@duration}{90 phút}
\newcommand{\@examdate}{}
\newcommand{\school}[1]{\renewcommand{\@school}{#1}}
\newcommand{\department}[1]{\renewcommand{\@department}{#1}}
\newcommand{\examtitle}[1]{\renewcommand{\@examtitle}{#1}}
\newcommand{\subject}[1]{\renewcommand{\@subject}{#1}}
\newcommand{\grade}[1]{\renewcommand{\@grade}{#1}}
\newcommand{\duration}[1]{\renewcommand{\@duration}{#1}}
\newcommand{\examdate}[1]{\renewcommand{\@examdate}{#1}}

% Answer-key toggle: \answerkeytrue / \answerkeyfalse
\newif\ifanswerkey
\answerkeyfalse

% ----- header -----
\newcommand{\makeheader}{%
  \thispagestyle{plain}%
  \noindent
  \begin{tabularx}{\textwidth}{@{}>{\centering\arraybackslash}X@{\hspace{0.8em}}>{\centering\arraybackslash}X@{}}
    {\fontsize{11}{13}\selectfont\bfseries\@department}\\[0.15em]
    {\fontsize{12}{14}\selectfont\bfseries\@school}\\[0.35em]
    {\footnotesize\textit{(Đề thi gồm \arabic{questiontotal} câu)} }
    &
    {\fontsize{12}{14}\selectfont\bfseries\@examtitle}\\[0.15em]
    {\fontsize{12}{14}\selectfont\bfseries Môn: \@subject
      \ifx\@grade\empty\else\ -- Lớp \@grade\fi}\\[0.15em]
    {\footnotesize Thời gian làm bài: \@duration\ (không kể thời gian phát đề)}\\[0.1em]
    \ifx\@examdate\empty\else{\footnotesize Ngày kiểm tra: \@examdate}\\\fi
  \end{tabularx}

  \vspace{0.55em}
  \noindent\rule{\textwidth}{0.6pt}\\[-0.15em]
  \noindent\rule{\textwidth}{0.25pt}

  \vspace{0.45em}
  \noindent
  \begin{tabularx}{\textwidth}{@{}X r@{}}
    Họ và tên: \dotfill & Số báo danh: \makebox[3.2cm]{\dotfill}\\[0.55em]
    Lớp: \makebox[3.6cm]{\dotfill} & Chữ ký GT: \makebox[3.2cm]{\dotfill}\\
  \end{tabularx}

  \ifanswerkey
    \vspace{0.4em}
    \noindent{\color{red!70!black}\bfseries ĐÁP ÁN VÀ HƯỚNG DẪN GIẢI}
    \par
  \fi
  \vspace{0.35em}
}

% Total question count (set by generator; fallback = last question number)
\newcounter{questiontotal}
\newcommand{\setquestiontotal}[1]{\setcounter{questiontotal}{#1}}

% ----- question / answer environments -----
\newcounter{question}
\renewcommand{\thequestion}{\arabic{question}}

\newenvironment{question}{%
  \par\addvspace{0.85em}%
  \refstepcounter{question}%
  \noindent\textbf{Câu \thequestion.}\hspace{0.4em}\ignorespaces
}{%
  \par\addvspace{0.25em}%
}

\newenvironment{dapan}{%
  \ifanswerkey
    \par\vspace{0.25em}%
    \noindent{\color{blue!60!black}\itshape Đáp án:}\hspace{0.35em}\ignorespaces
  \else
    \setbox0=\vbox\bgroup\color{white}%
  \fi
}{%
  \ifanswerkey
    \par
  \else
    \egroup
  \fi
}

\newenvironment{loigiai}{%
  \ifanswerkey
    \par\vspace{0.2em}%
    \noindent{\small\bfseries Lời giải.}\\[0.15em]
    \begingroup\small
  \else
    \setbox0=\vbox\bgroup\color{white}%
  \fi
}{%
  \ifanswerkey
    \endgroup\par
  \else
    \egroup
  \fi
}

% Multiple-choice helper used in some bank items
\newenvironment{fourchoices}{%
  \begin{enumerate}[label=\textbf{\Alph*.}, leftmargin=1.6em, itemsep=0.15em, topsep=0.25em]
}{%
  \end{enumerate}
}

\endinput
